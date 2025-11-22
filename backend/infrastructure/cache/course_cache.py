"""
Course Cache Service

코스 생성 결과를 캐싱하는 서비스입니다.
"""

import logging
from typing import Optional

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.cache.redis_cache import get_cache

logger = logging.getLogger(__name__)


class CourseCacheService:
    """
    코스 캐시 서비스
    
    코스 생성 결과를 Redis에 캐싱하여 성능을 최적화합니다.
    """

    # TTL 설정 (초 단위)
    COURSE_CACHE_TTL = 24 * 60 * 60  # 24시간
    ROUTE_CACHE_TTL = 7 * 24 * 60 * 60  # 7일

    @staticmethod
    def _generate_course_key(
        latitude: float,
        longitude: float,
        distance: float,
    ) -> str:
        """
        코스 캐시 키를 생성합니다.
        
        Args:
            latitude: 시작 위도
            longitude: 시작 경도
            distance: 목표 거리 (km)
            
        Returns:
            캐시 키
        """
        # 소수점 4자리까지 반올림하여 키 생성 (약 11m 정밀도)
        # format을 사용하여 항상 4자리 소수점 표시
        lat_str = f"{latitude:.4f}".rstrip('0').rstrip('.')
        lon_str = f"{longitude:.4f}".rstrip('0').rstrip('.')
        dist_str = f"{distance:.1f}".rstrip('0').rstrip('.')
        return f"course:{lat_str}:{lon_str}:{dist_str}"

    @staticmethod
    def _generate_route_key(
        start: Coordinate,
        end: Coordinate,
    ) -> str:
        """
        라우팅 결과 캐시 키를 생성합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            
        Returns:
            캐시 키
        """
        # 소수점 4자리까지 반올림하여 키 생성
        # format을 사용하여 항상 4자리 소수점 표시
        start_lat_str = f"{start.latitude:.4f}".rstrip('0').rstrip('.')
        start_lon_str = f"{start.longitude:.4f}".rstrip('0').rstrip('.')
        end_lat_str = f"{end.latitude:.4f}".rstrip('0').rstrip('.')
        end_lon_str = f"{end.longitude:.4f}".rstrip('0').rstrip('.')
        return f"route:{start_lat_str}:{start_lon_str}:{end_lat_str}:{end_lon_str}"

    @staticmethod
    async def get_course(
        latitude: float,
        longitude: float,
        distance: float,
    ) -> Optional[dict]:
        """
        캐시에서 코스를 조회합니다.
        
        Args:
            latitude: 시작 위도
            longitude: 시작 경도
            distance: 목표 거리 (km)
            
        Returns:
            캐시된 코스 데이터 (없으면 None)
        """
        try:
            cache = await get_cache()
            key = CourseCacheService._generate_course_key(
                latitude, longitude, distance
            )
            result = await cache.get(key)
            
            if result:
                logger.debug(
                    f"코스 캐시 히트 (key={key})"
                )
            return result
        except Exception as e:
            logger.error(f"코스 캐시 조회 오류: {e}")
            return None

    @staticmethod
    async def set_course(
        latitude: float,
        longitude: float,
        distance: float,
        course_data: dict,
    ) -> bool:
        """
        코스를 캐시에 저장합니다.
        
        Args:
            latitude: 시작 위도
            longitude: 시작 경도
            distance: 목표 거리 (km)
            course_data: 코스 데이터
            
        Returns:
            저장 성공 여부
        """
        try:
            cache = await get_cache()
            key = CourseCacheService._generate_course_key(
                latitude, longitude, distance
            )
            success = await cache.set(
                key,
                course_data,
                ttl=CourseCacheService.COURSE_CACHE_TTL,
            )
            
            if success:
                logger.debug(
                    f"코스 캐시 저장 성공 (key={key}, ttl={CourseCacheService.COURSE_CACHE_TTL}s)"
                )
            return success
        except Exception as e:
            logger.error(f"코스 캐시 저장 오류: {e}")
            return False

    @staticmethod
    async def get_route(
        start: Coordinate,
        end: Coordinate,
    ) -> Optional[list]:
        """
        캐시에서 라우팅 결과를 조회합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            
        Returns:
            캐시된 라우팅 결과 (없으면 None)
        """
        try:
            cache = await get_cache()
            key = CourseCacheService._generate_route_key(start, end)
            result = await cache.get(key)
            
            if result:
                logger.debug(f"라우팅 캐시 히트 (key={key})")
            return result
        except Exception as e:
            logger.error(f"라우팅 캐시 조회 오류: {e}")
            return None

    @staticmethod
    async def set_route(
        start: Coordinate,
        end: Coordinate,
        route_data: list,
    ) -> bool:
        """
        라우팅 결과를 캐시에 저장합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            route_data: 라우팅 결과 (좌표 배열)
            
        Returns:
            저장 성공 여부
        """
        try:
            cache = await get_cache()
            key = CourseCacheService._generate_route_key(start, end)
            
            # 좌표 배열을 딕셔너리 리스트로 변환
            route_dict = [
                {"latitude": coord.latitude, "longitude": coord.longitude}
                if isinstance(coord, Coordinate)
                else coord
                for coord in route_data
            ]
            
            success = await cache.set(
                key,
                route_dict,
                ttl=CourseCacheService.ROUTE_CACHE_TTL,
            )
            
            if success:
                logger.debug(
                    f"라우팅 캐시 저장 성공 (key={key}, ttl={CourseCacheService.ROUTE_CACHE_TTL}s)"
                )
            return success
        except Exception as e:
            logger.error(f"라우팅 캐시 저장 오류: {e}")
            return False

    @staticmethod
    async def clear_course_cache(
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
    ) -> int:
        """
        코스 캐시를 삭제합니다.
        
        Args:
            latitude: 시작 위도 (None이면 모든 코스 캐시 삭제)
            longitude: 시작 경도 (None이면 모든 코스 캐시 삭제)
            
        Returns:
            삭제된 키의 개수
        """
        try:
            cache = await get_cache()
            if latitude is not None and longitude is not None:
                # 특정 위치의 캐시만 삭제
                pattern = f"course:{round(latitude, 4)}:{round(longitude, 4)}:*"
            else:
                # 모든 코스 캐시 삭제
                pattern = "course:*"
            
            return await cache.clear_pattern(pattern)
        except Exception as e:
            logger.error(f"코스 캐시 삭제 오류: {e}")
            return 0

