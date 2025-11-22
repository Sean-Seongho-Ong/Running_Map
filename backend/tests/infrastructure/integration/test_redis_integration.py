"""
Redis Integration Tests

실제 Redis 연결 및 캐시 동작을 테스트합니다.
"""

import pytest
import json

from infrastructure.cache.redis_cache import get_cache, close_cache
from infrastructure.cache.course_cache import CourseCacheService
from domain.value_objects.coordinate import Coordinate


@pytest.mark.asyncio
@pytest.mark.integration
class TestRedisConnection:
    """Redis 연결 테스트"""

    async def test_redis_connection(self):
        """Redis 연결 확인"""
        cache = await get_cache()
        result = await cache.client.ping()
        assert result is True
        await close_cache()

    async def test_redis_basic_operations(self):
        """Redis 기본 동작 테스트"""
        cache = await get_cache()

        # 저장
        test_key = "integration:test:key"
        test_value = {"test": "value", "number": 123}
        success = await cache.set(test_key, test_value, ttl=60)
        assert success is True

        # 조회
        retrieved = await cache.get(test_key)
        assert retrieved == test_value

        # 존재 확인
        exists = await cache.exists(test_key)
        assert exists is True

        # 삭제
        deleted = await cache.delete(test_key)
        assert deleted is True

        # 삭제 확인
        exists_after = await cache.exists(test_key)
        assert exists_after is False

        await close_cache()


@pytest.mark.asyncio
@pytest.mark.integration
class TestCourseCacheIntegration:
    """CourseCacheService 통합 테스트"""

    async def test_course_cache_set_and_get(self):
        """코스 캐시 저장 및 조회 테스트"""
        course_data = {
            "name": "캐시 테스트 코스",
            "distance": 10.0,
            "polyline": [
                {"latitude": 37.5665, "longitude": 126.9780},
                {"latitude": 37.5670, "longitude": 126.9785},
            ],
        }

        # 저장
        success = await CourseCacheService.set_course(
            37.5665, 126.9780, 10.0, course_data
        )
        assert success is True

        # 조회
        retrieved = await CourseCacheService.get_course(37.5665, 126.9780, 10.0)
        assert retrieved is not None
        assert retrieved["name"] == "캐시 테스트 코스"
        assert retrieved["distance"] == 10.0

        # 정리
        await CourseCacheService.clear_course_cache(37.5665, 126.9780)
        await close_cache()

    async def test_route_cache_set_and_get(self):
        """라우팅 캐시 저장 및 조회 테스트"""
        start = Coordinate(latitude=37.5665, longitude=126.9780)
        end = Coordinate(latitude=37.5670, longitude=126.9785)

        route_data = [
            Coordinate(latitude=37.5665, longitude=126.9780),
            Coordinate(latitude=37.5667, longitude=126.9782),
            Coordinate(latitude=37.5670, longitude=126.9785),
        ]

        # 저장
        success = await CourseCacheService.set_route(start, end, route_data)
        assert success is True

        # 조회
        retrieved = await CourseCacheService.get_route(start, end)
        assert retrieved is not None
        assert len(retrieved) == 3
        assert retrieved[0]["latitude"] == 37.5665
        assert retrieved[0]["longitude"] == 126.9780

        await close_cache()

    async def test_cache_key_generation(self):
        """캐시 키 생성 테스트"""
        # 코스 캐시 키
        course_key = CourseCacheService._generate_course_key(37.5665, 126.9780, 10.0)
        assert course_key.startswith("course:")
        assert "37.5665" in course_key
        assert "10" in course_key

        # 라우팅 캐시 키
        start = Coordinate(latitude=37.5665, longitude=126.9780)
        end = Coordinate(latitude=37.5670, longitude=126.9785)
        route_key = CourseCacheService._generate_route_key(start, end)
        assert route_key.startswith("route:")
        assert "37.5665" in route_key
        # 소수점 반올림으로 인해 "37.567" 또는 "37.5670" 모두 가능
        assert "37.567" in route_key

    async def test_cache_clear_pattern(self):
        """캐시 패턴 삭제 테스트"""
        cache = await get_cache()

        # 여러 키 생성
        for i in range(3):
            key = f"integration:test:pattern:{i}"
            await cache.set(key, {"value": i}, ttl=60)

        # 패턴으로 삭제
        deleted_count = await cache.clear_pattern("integration:test:pattern:*")
        assert deleted_count == 3

        # 삭제 확인
        for i in range(3):
            key = f"integration:test:pattern:{i}"
            exists = await cache.exists(key)
            assert exists is False

        await close_cache()

