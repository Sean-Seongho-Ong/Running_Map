"""
Save Course Use Case Tests

코스 저장 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.course import Course, CourseMetadata
from domain.repositories.course_repository import CourseRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

from application.dto.course_dto import CourseSaveRequestDTO, CoordinateDTO
from application.use_cases.save_course import SaveCourseUseCase
from infrastructure.exceptions import DatabaseError


class TestSaveCourseUseCase:
    """SaveCourseUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock CourseRepository"""
        return AsyncMock(spec=CourseRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return SaveCourseUseCase(course_repository=mock_repository)

    @pytest.fixture
    def request_dto(self):
        """테스트용 요청 DTO"""
        polyline = [
            CoordinateDTO(latitude=37.5665, longitude=126.9780),
            CoordinateDTO(latitude=37.5670, longitude=126.9785),
        ]
        return CourseSaveRequestDTO(
            name="테스트 코스",
            polyline=polyline,
            distance=5.0,
            is_public=True,
        )

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, request_dto, mock_repository):
        """코스 저장 성공 테스트"""
        # Mock 설정
        saved_course = Course(
            name=request_dto.name,
            polyline=[coord.to_domain() for coord in request_dto.polyline],
            distance=Distance.from_kilometers(request_dto.distance),
            is_public=request_dto.is_public,
        )
        mock_repository.create.return_value = saved_course

        # 실행
        response = await use_case.execute(request_dto)

        # 검증
        assert response.id == saved_course.id
        assert response.name == request_dto.name
        mock_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_database_error(self, use_case, request_dto, mock_repository):
        """데이터베이스 오류 테스트"""
        mock_repository.create.side_effect = DatabaseError("데이터베이스 오류")

        with pytest.raises(DatabaseError):
            await use_case.execute(request_dto)

