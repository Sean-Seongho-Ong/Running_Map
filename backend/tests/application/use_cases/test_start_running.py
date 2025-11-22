"""
Start Running Use Case Tests

러닝 시작 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.running_session import RunningSession
from domain.repositories.course_repository import CourseRepository
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate

from application.dto.running_dto import (
    RunningSessionStartRequestDTO,
    CoordinateDTO,
)
from application.use_cases.start_running import StartRunningUseCase
from infrastructure.exceptions import DatabaseError


class TestStartRunningUseCase:
    """StartRunningUseCase 테스트"""

    @pytest.fixture
    def mock_session_repository(self):
        """Mock RunningSessionRepository"""
        return AsyncMock(spec=RunningSessionRepository)

    @pytest.fixture
    def mock_course_repository(self):
        """Mock CourseRepository"""
        return AsyncMock(spec=CourseRepository)

    @pytest.fixture
    def use_case(self, mock_session_repository, mock_course_repository):
        """Use Case 인스턴스"""
        return StartRunningUseCase(
            running_session_repository=mock_session_repository,
            course_repository=mock_course_repository,
        )

    @pytest.fixture
    def request_dto(self):
        """테스트용 요청 DTO"""
        start_location = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        return RunningSessionStartRequestDTO(start_location=start_location)

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, request_dto, mock_session_repository):
        """러닝 세션 시작 성공 테스트"""
        # Mock 설정
        session = RunningSession(
            start_location=request_dto.start_location.to_domain()
        )
        mock_session_repository.create.return_value = session

        # 실행
        response = await use_case.execute(request_dto)

        # 검증
        assert response.session_id == session.id
        assert response.started_at == session.started_at
        mock_session_repository.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_with_course_id(self, use_case, mock_session_repository, mock_course_repository):
        """코스 ID 포함 시작 테스트"""
        from domain.entities.course import Course
        from domain.value_objects.distance import Distance

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

        start_location = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        request = RunningSessionStartRequestDTO(
            start_location=start_location, course_id=course_id
        )

        mock_course_repository.get_by_id.return_value = course
        session = RunningSession(
            start_location=start_location.to_domain(), course_id=course_id
        )
        mock_session_repository.create.return_value = session

        response = await use_case.execute(request)

        assert response.session_id == session.id
        mock_course_repository.get_by_id.assert_called_once_with(course_id)

    @pytest.mark.asyncio
    async def test_execute_course_not_found(self, use_case, mock_course_repository):
        """코스 없음 테스트"""
        course_id = uuid4()
        start_location = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        request = RunningSessionStartRequestDTO(
            start_location=start_location, course_id=course_id
        )

        mock_course_repository.get_by_id.return_value = None

        with pytest.raises(ValueError, match="코스를 찾을 수 없습니다"):
            await use_case.execute(request)

