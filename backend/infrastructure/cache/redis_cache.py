"""
Redis Cache Implementation

Redis를 사용한 캐시 구현입니다.
비동기 Redis 클라이언트를 사용하여 성능을 최적화합니다.
"""

import json
import logging
from typing import Optional, Any

import redis.asyncio as aioredis
from redis.asyncio import Redis
from redis.exceptions import RedisError

from infrastructure.config.settings import settings

logger = logging.getLogger(__name__)


class RedisCache:
    """
    Redis 캐시 클래스
    
    비동기 Redis 클라이언트를 사용하여 캐시를 관리합니다.
    """

    def __init__(self, redis_url: Optional[str] = None):
        """
        Args:
            redis_url: Redis 연결 URL (기본값: settings.redis_url)
        """
        self.redis_url = redis_url or settings.redis_url
        self._client: Optional[Redis] = None
        self._connection_pool: Optional[aioredis.ConnectionPool] = None

    async def connect(self) -> None:
        """Redis 연결을 초기화합니다."""
        try:
            self._connection_pool = aioredis.ConnectionPool.from_url(
                self.redis_url,
                max_connections=10,
                decode_responses=True,
            )
            self._client = aioredis.Redis(connection_pool=self._connection_pool)
            
            # 연결 테스트
            await self._client.ping()
            logger.info(f"Redis 연결 성공: {self.redis_url}")
        except RedisError as e:
            logger.error(f"Redis 연결 실패: {e}")
            raise

    async def disconnect(self) -> None:
        """Redis 연결을 종료합니다."""
        if self._client:
            await self._client.aclose()
        if self._connection_pool:
            await self._connection_pool.disconnect()
        logger.info("Redis 연결 종료")

    @property
    def client(self) -> Redis:
        """
        Redis 클라이언트를 반환합니다.
        
        Returns:
            Redis 클라이언트
            
        Raises:
            RuntimeError: 연결되지 않은 경우
        """
        if self._client is None:
            raise RuntimeError("Redis가 연결되지 않았습니다. connect()를 먼저 호출하세요.")
        return self._client

    async def get(self, key: str) -> Optional[Any]:
        """
        캐시에서 값을 조회합니다.
        
        Args:
            key: 캐시 키
            
        Returns:
            캐시된 값 (없으면 None)
        """
        try:
            value = await self.client.get(key)
            if value is None:
                return None
            
            # JSON 문자열을 파싱
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                # JSON이 아니면 문자열 그대로 반환
                return value
        except RedisError as e:
            logger.error(f"Redis get 오류 (key={key}): {e}")
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        캐시에 값을 저장합니다.
        
        Args:
            key: 캐시 키
            value: 저장할 값
            ttl: Time To Live (초 단위, None이면 만료 없음)
            
        Returns:
            저장 성공 여부
        """
        try:
            # 값이 dict나 list면 JSON으로 변환
            if isinstance(value, (dict, list)):
                value_str = json.dumps(value, ensure_ascii=False)
            else:
                value_str = str(value)

            if ttl is not None:
                await self.client.setex(key, ttl, value_str)
            else:
                await self.client.set(key, value_str)

            logger.debug(f"Redis set 성공 (key={key}, ttl={ttl})")
            return True
        except RedisError as e:
            logger.error(f"Redis set 오류 (key={key}): {e}")
            return False

    async def delete(self, key: str) -> bool:
        """
        캐시에서 값을 삭제합니다.
        
        Args:
            key: 캐시 키
            
        Returns:
            삭제 성공 여부
        """
        try:
            result = await self.client.delete(key)
            logger.debug(f"Redis delete 성공 (key={key})")
            return result > 0
        except RedisError as e:
            logger.error(f"Redis delete 오류 (key={key}): {e}")
            return False

    async def exists(self, key: str) -> bool:
        """
        캐시 키의 존재 여부를 확인합니다.
        
        Args:
            key: 캐시 키
            
        Returns:
            존재 여부
        """
        try:
            result = await self.client.exists(key)
            return result > 0
        except RedisError as e:
            logger.error(f"Redis exists 오류 (key={key}): {e}")
            return False

    async def clear_pattern(self, pattern: str) -> int:
        """
        패턴에 맞는 모든 키를 삭제합니다.
        
        Args:
            pattern: 키 패턴 (예: "course:*")
            
        Returns:
            삭제된 키의 개수
        """
        try:
            keys = []
            async for key in self.client.scan_iter(match=pattern):
                keys.append(key)

            if keys:
                deleted = await self.client.delete(*keys)
                logger.info(f"Redis 패턴 삭제 성공 (pattern={pattern}, count={deleted})")
                return deleted
            return 0
        except RedisError as e:
            logger.error(f"Redis clear_pattern 오류 (pattern={pattern}): {e}")
            return 0


# 전역 Redis 캐시 인스턴스
_cache: Optional[RedisCache] = None


async def get_cache() -> RedisCache:
    """
    전역 Redis 캐시 인스턴스를 반환합니다.
    
    Returns:
        RedisCache 인스턴스
    """
    global _cache
    if _cache is None:
        _cache = RedisCache()
        await _cache.connect()
    return _cache


async def close_cache() -> None:
    """전역 Redis 캐시 연결을 종료합니다."""
    global _cache
    if _cache is not None:
        await _cache.disconnect()
        _cache = None

