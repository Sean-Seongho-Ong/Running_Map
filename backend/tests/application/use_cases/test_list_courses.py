"""
List Courses Use Case Tests

코스 목록 조회 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.course import Course
from domain.repositories.course_repository import CourseRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

from application.use_cases.list_courses import ListCoursesUseCase
from infrastructure.exceptions import DatabaseError


class TestListCoursesUseCase:
    """ListCoursesUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock CourseRepository"""
        return AsyncMock(spec=CourseRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return ListCoursesUseCase(course_repository=mock_repository)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository):
        """코스 목록 조회 성공 테스트"""
        # Mock 설정
        courses = [
            Course(
                name="코스 1",
                polyline=[
                    Coordinate(latitude=37.5665, longitude=126.9780),
                    Coordinate(latitude=37.5670, longitude=126.9785),
                ],
                distance=Distance.from_kilometers(5.0),
            ),
            Course(
                name="코스 2",
                polyline=[
                    Coordinate(latitude=37.5680, longitude=126.9790),
                    Coordinate(latitude=37.5690, longitude=126.9800),
                ],
                distance=Distance.from_kilometers(10.0),
            ),
        ]
        mock_repository.list.return_value = courses

        # 실행
        response = await use_case.execute(limit=20, offset=0)

        # 검증
        assert len(response.courses) == 2
        assert response.limit == 20
        assert response.offset == 0
        mock_repository.list.assert_called_once_with(
            user_id=None, is_public=None, limit=20, offset=0
        )

    @pytest.mark.asyncio
    async def test_execute_with_filters(self, use_case, mock_repository):
        """필터 포함 조회 테스트"""
        user_id = uuid4()
        courses = []
        mock_repository.list.return_value = courses

        response = await use_case.execute(
            user_id=user_id, is_public=True, limit=10, offset=5
        )

        assert len(response.courses) == 0
        mock_repository.list.assert_called_once_with(
            user_id=user_id, is_public=True, limit=10, offset=5
        )

