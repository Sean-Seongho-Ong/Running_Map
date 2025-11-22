"""
Generate Course Use Case Tests

코스 생성 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from domain.entities.route import Route
from domain.services.loop_generator import LoopGenerator, LoopGenerationError
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

from application.dto.course_dto import (
    CourseGenerationRequestDTO,
    CourseGenerationParametersDTO,
)
from application.dto.course_dto import CoordinateDTO
from application.use_cases.generate_course import GenerateCourseUseCase
from infrastructure.cache.course_cache import CourseCacheService


class MockLoopGenerator(LoopGenerator):
    """테스트용 Mock LoopGenerator"""

    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail

    async def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: dict | None = None,
    ) -> Route:
        """Mock 루프 생성"""
        if self.should_fail:
            raise LoopGenerationError("루프 생성 실패")

        # 간단한 더미 루프 생성
        polyline = [
            start_point,
            Coordinate(
                latitude=start_point.latitude + 0.01,
                longitude=start_point.longitude + 0.01,
            ),
            Coordinate(
                latitude=start_point.latitude + 0.02,
                longitude=start_point.longitude + 0.02,
            ),
            start_point,  # 루프 닫기
        ]

        return Route(
            polyline=polyline,
            distance=target_distance,
            algorithm="STEP_ADAPTIVE",
            iterations=3,
            step_used=1.0,
            relative_error=0.05,
        )


class TestGenerateCourseUseCase:
    """GenerateCourseUseCase 테스트"""

    @pytest.fixture
    def mock_loop_generator(self):
        """Mock LoopGenerator"""
        return MockLoopGenerator()

    @pytest.fixture
    def use_case(self, mock_loop_generator):
        """Use Case 인스턴스"""
        return GenerateCourseUseCase(loop_generator=mock_loop_generator)

    @pytest.fixture
    def request_dto(self):
        """테스트용 요청 DTO"""
        start_point = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        return CourseGenerationRequestDTO(
            start_point=start_point, target_distance=10.0
        )

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, request_dto):
        """코스 생성 성공 테스트"""
        with patch.object(
            CourseCacheService, "get_course", return_value=None
        ) as mock_get_cache, patch.object(
            CourseCacheService, "set_course", return_value=True
        ) as mock_set_cache:
            response = await use_case.execute(request_dto)

            assert response.status == "OK"
            assert response.course is not None
            assert response.course.algorithm == "STEP_ADAPTIVE"
            assert response.course.distance == 10.0
            mock_get_cache.assert_called_once()
            mock_set_cache.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_cache_hit(self, use_case, request_dto):
        """캐시 히트 테스트"""
        cached_result = {
            "id": str(uuid4()),
            "polyline": [
                {"latitude": 37.5665, "longitude": 126.9780},
                {"latitude": 37.5670, "longitude": 126.9785},
            ],
            "distance": 10.0,
            "relative_error": 0.05,
            "algorithm": "STEP_ADAPTIVE",
            "iterations": 3,
            "step_used": 1.0,
            "metadata": None,
        }

        with patch.object(
            CourseCacheService, "get_course", return_value=cached_result
        ) as mock_get_cache, patch.object(
            CourseCacheService, "set_course"
        ) as mock_set_cache:
            response = await use_case.execute(request_dto)

            assert response.status == "OK"
            assert response.course is not None
            assert response.course.distance == 10.0
            mock_get_cache.assert_called_once()
            mock_set_cache.assert_not_called()  # 캐시 히트 시 저장하지 않음

    @pytest.mark.asyncio
    async def test_execute_generation_failure(self, request_dto):
        """코스 생성 실패 테스트"""
        failing_generator = MockLoopGenerator(should_fail=True)
        use_case = GenerateCourseUseCase(loop_generator=failing_generator)

        with patch.object(
            CourseCacheService, "get_course", return_value=None
        ):
            response = await use_case.execute(request_dto)

            assert response.status == "FAIL"
            assert response.course is None
            assert response.error is not None
            assert response.error["code"] == "COURSE_GENERATION_FAILED"

    @pytest.mark.asyncio
    async def test_execute_with_parameters(self, use_case):
        """파라미터 포함 요청 테스트"""
        start_point = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        parameters = CourseGenerationParametersDTO(step_init=1.5, max_iter=10)
        request = CourseGenerationRequestDTO(
            start_point=start_point,
            target_distance=10.0,
            parameters=parameters,
        )

        with patch.object(
            CourseCacheService, "get_course", return_value=None
        ), patch.object(CourseCacheService, "set_course", return_value=True):
            response = await use_case.execute(request)

            assert response.status == "OK"
            assert response.course is not None

