"""
Get Course Use Case Tests

코스 상세 조회 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.course import Course
from domain.repositories.course_repository import CourseRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

from application.use_cases.get_course import GetCourseUseCase


class TestGetCourseUseCase:
    """GetCourseUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock CourseRepository"""
        return AsyncMock(spec=CourseRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return GetCourseUseCase(course_repository=mock_repository)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository):
        """코스 상세 조회 성공 테스트"""
        course_id = uuid4()
        course = Course(
            name="테스트 코스",
            polyline=[
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
            ],
            distance=Distance.from_kilometers(5.0),
        )
        course.id = course_id
        mock_repository.get_by_id.return_value = course

        response = await use_case.execute(course_id)

        assert response is not None
        assert response.id == course_id
        assert response.name == "테스트 코스"
        mock_repository.get_by_id.assert_called_once_with(course_id)

    @pytest.mark.asyncio
    async def test_execute_not_found(self, use_case, mock_repository):
        """코스 없음 테스트"""
        course_id = uuid4()
        mock_repository.get_by_id.return_value = None

        response = await use_case.execute(course_id)

        assert response is None
        mock_repository.get_by_id.assert_called_once_with(course_id)

