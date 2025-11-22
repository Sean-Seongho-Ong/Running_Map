"""
Delete Course Use Case Tests

코스 삭제 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.repositories.course_repository import CourseRepository

from application.use_cases.delete_course import DeleteCourseUseCase
from infrastructure.exceptions import DatabaseError


class TestDeleteCourseUseCase:
    """DeleteCourseUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock CourseRepository"""
        return AsyncMock(spec=CourseRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return DeleteCourseUseCase(course_repository=mock_repository)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository):
        """코스 삭제 성공 테스트"""
        course_id = uuid4()
        mock_repository.delete.return_value = True

        response = await use_case.execute(course_id)

        assert response.success is True
        assert response.course_id == course_id
        mock_repository.delete.assert_called_once_with(course_id)

    @pytest.mark.asyncio
    async def test_execute_not_found(self, use_case, mock_repository):
        """코스 없음 테스트"""
        course_id = uuid4()
        mock_repository.delete.return_value = False

        response = await use_case.execute(course_id)

        assert response.success is False
        assert response.course_id == course_id

