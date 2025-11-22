"""
Redis Cache Tests

Redis 캐시 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import json

from infrastructure.cache.redis_cache import RedisCache
from infrastructure.cache.course_cache import CourseCacheService
from domain.value_objects.coordinate import Coordinate
from infrastructure.exceptions import CacheError


class TestRedisCache:
    """RedisCache 테스트"""

    @pytest.fixture
    def cache(self):
        """RedisCache 인스턴스"""
        return RedisCache(redis_url="redis://localhost:6379/0")

    @pytest.fixture
    def mock_redis_client(self):
        """Mock Redis 클라이언트"""
        client = AsyncMock()
        client.ping = AsyncMock(return_value=True)
        client.get = AsyncMock(return_value=None)
        client.set = AsyncMock(return_value=True)
        client.setex = AsyncMock(return_value=True)
        client.delete = AsyncMock(return_value=1)
        client.exists = AsyncMock(return_value=0)
        client.scan_iter = AsyncMock(return_value=iter([]))
        client.close = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_connect_success(self, cache, mock_redis_client):
        """Redis 연결 성공 테스트"""
        with patch("infrastructure.cache.redis_cache.aioredis.ConnectionPool") as mock_pool:
            mock_pool.from_url.return_value = MagicMock()
            with patch("infrastructure.cache.redis_cache.aioredis.Redis") as mock_redis:
                mock_redis.return_value = mock_redis_client

                await cache.connect()

                assert cache._client is not None

    @pytest.mark.asyncio
    async def test_get_success(self, cache, mock_redis_client):
        """캐시 조회 성공 테스트"""
        cache._client = mock_redis_client
        test_value = json.dumps({"key": "value"})
        mock_redis_client.get.return_value = test_value

        result = await cache.get("test:key")

        assert result == {"key": "value"}
        mock_redis_client.get.assert_called_once_with("test:key")

    @pytest.mark.asyncio
    async def test_get_not_found(self, cache, mock_redis_client):
        """캐시 조회 - 없음 테스트"""
        cache._client = mock_redis_client
        mock_redis_client.get.return_value = None

        result = await cache.get("test:key")

        assert result is None

    @pytest.mark.asyncio
    async def test_set_success(self, cache, mock_redis_client):
        """캐시 저장 성공 테스트"""
        cache._client = mock_redis_client
        test_value = {"key": "value"}

        result = await cache.set("test:key", test_value, ttl=60)

        assert result is True
        mock_redis_client.setex.assert_called_once()

    @pytest.mark.asyncio
    async def test_set_without_ttl(self, cache, mock_redis_client):
        """캐시 저장 - TTL 없음 테스트"""
        cache._client = mock_redis_client
        test_value = {"key": "value"}

        result = await cache.set("test:key", test_value)

        assert result is True
        mock_redis_client.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_success(self, cache, mock_redis_client):
        """캐시 삭제 성공 테스트"""
        cache._client = mock_redis_client
        mock_redis_client.delete.return_value = 1

        result = await cache.delete("test:key")

        assert result is True
        mock_redis_client.delete.assert_called_once_with("test:key")

    @pytest.mark.asyncio
    async def test_exists_true(self, cache, mock_redis_client):
        """캐시 존재 확인 - 있음 테스트"""
        cache._client = mock_redis_client
        mock_redis_client.exists.return_value = 1

        result = await cache.exists("test:key")

        assert result is True

    @pytest.mark.asyncio
    async def test_exists_false(self, cache, mock_redis_client):
        """캐시 존재 확인 - 없음 테스트"""
        cache._client = mock_redis_client
        mock_redis_client.exists.return_value = 0

        result = await cache.exists("test:key")

        assert result is False


class TestCourseCacheService:
    """CourseCacheService 테스트"""

    @pytest.fixture
    def sample_coordinate(self):
        """샘플 좌표"""
        return Coordinate(latitude=37.5665, longitude=126.9780)

    @pytest.mark.asyncio
    async def test_generate_course_key(self):
        """코스 캐시 키 생성 테스트"""
        key = CourseCacheService._generate_course_key(37.5665, 126.9780, 10.0)
        # 소수점 0 제거 후 비교
        assert key.startswith("course:37.5665:")
        assert "10" in key or "10.0" in key

    @pytest.mark.asyncio
    async def test_generate_route_key(self, sample_coordinate):
        """라우팅 캐시 키 생성 테스트"""
        end = Coordinate(latitude=37.5670, longitude=126.9785)
        key = CourseCacheService._generate_route_key(sample_coordinate, end)
        # 소수점 0 제거 후 비교
        assert key.startswith("route:37.5665:")
        assert "37.567" in key or "37.5670" in key

    @pytest.mark.asyncio
    async def test_get_course_success(self, sample_coordinate):
        """코스 캐시 조회 성공 테스트"""
        course_data = {"name": "테스트 코스", "distance": 10.0}

        with patch("infrastructure.cache.course_cache.get_cache") as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.get = AsyncMock(return_value=course_data)
            mock_get_cache.return_value = mock_cache

            result = await CourseCacheService.get_course(37.5665, 126.9780, 10.0)

            assert result == course_data

    @pytest.mark.asyncio
    async def test_set_course_success(self, sample_coordinate):
        """코스 캐시 저장 성공 테스트"""
        course_data = {"name": "테스트 코스", "distance": 10.0}

        with patch("infrastructure.cache.course_cache.get_cache") as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.set = AsyncMock(return_value=True)
            mock_get_cache.return_value = mock_cache

            result = await CourseCacheService.set_course(
                37.5665, 126.9780, 10.0, course_data
            )

            assert result is True
            mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_route_success(self, sample_coordinate):
        """라우팅 캐시 조회 성공 테스트"""
        end = Coordinate(latitude=37.5670, longitude=126.9785)
        route_data = [
            {"latitude": 37.5665, "longitude": 126.9780},
            {"latitude": 37.5670, "longitude": 126.9785},
        ]

        with patch("infrastructure.cache.course_cache.get_cache") as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.get = AsyncMock(return_value=route_data)
            mock_get_cache.return_value = mock_cache

            result = await CourseCacheService.get_route(sample_coordinate, end)

            assert result == route_data

    @pytest.mark.asyncio
    async def test_set_route_success(self, sample_coordinate):
        """라우팅 캐시 저장 성공 테스트"""
        end = Coordinate(latitude=37.5670, longitude=126.9785)
        route_data = [sample_coordinate, end]

        with patch("infrastructure.cache.course_cache.get_cache") as mock_get_cache:
            mock_cache = AsyncMock()
            mock_cache.set = AsyncMock(return_value=True)
            mock_get_cache.return_value = mock_cache

            result = await CourseCacheService.set_route(sample_coordinate, end, route_data)

            assert result is True
            mock_cache.set.assert_called_once()

