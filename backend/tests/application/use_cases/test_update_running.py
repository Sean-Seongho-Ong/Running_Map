"""
Update Running Use Case Tests

러닝 업데이트 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.running_session import RunningSession
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate

from application.dto.running_dto import (
    RunningSessionUpdateRequestDTO,
    CoordinateDTO,
    RunningStatsDTO,
)
from application.use_cases.update_running import UpdateRunningUseCase
from infrastructure.exceptions import DatabaseError


class TestUpdateRunningUseCase:
    """UpdateRunningUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock RunningSessionRepository"""
        return AsyncMock(spec=RunningSessionRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return UpdateRunningUseCase(running_session_repository=mock_repository)

    @pytest.fixture
    def session(self):
        """테스트용 RunningSession"""
        return RunningSession(
            start_location=Coordinate(latitude=37.5665, longitude=126.9780)
        )

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository, session):
        """러닝 세션 업데이트 성공 테스트"""
        session_id = session.id
        mock_repository.get_by_id.return_value = session
        mock_repository.update.return_value = session

        request = RunningSessionUpdateRequestDTO(
            current_location=CoordinateDTO(latitude=37.5670, longitude=126.9785),
            stats=RunningStatsDTO(
                distance=5.0,
                duration=1800,
                pace=6.0,
                speed=10.0,
                elevation_gain=0.0,
                elevation_loss=0.0,
            ),
        )

        response = await use_case.execute(session_id, request)

        assert response.session_id == session_id
        mock_repository.get_by_id.assert_called_once_with(session_id)
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_session_not_found(self, use_case, mock_repository):
        """세션 없음 테스트"""
        session_id = uuid4()
        mock_repository.get_by_id.return_value = None

        request = RunningSessionUpdateRequestDTO()

        with pytest.raises(ValueError, match="러닝 세션을 찾을 수 없습니다"):
            await use_case.execute(session_id, request)

