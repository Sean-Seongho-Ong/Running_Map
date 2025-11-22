"""
Finish Running Use Case Tests

러닝 종료 Use Case의 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from domain.entities.running_session import RunningSession
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate

from application.dto.running_dto import (
    RunningSessionFinishRequestDTO,
    CoordinateDTO,
)
from application.use_cases.finish_running import FinishRunningUseCase


class TestFinishRunningUseCase:
    """FinishRunningUseCase 테스트"""

    @pytest.fixture
    def mock_repository(self):
        """Mock RunningSessionRepository"""
        return AsyncMock(spec=RunningSessionRepository)

    @pytest.fixture
    def use_case(self, mock_repository):
        """Use Case 인스턴스"""
        return FinishRunningUseCase(running_session_repository=mock_repository)

    @pytest.fixture
    def session(self):
        """테스트용 RunningSession"""
        return RunningSession(
            start_location=Coordinate(latitude=37.5665, longitude=126.9780)
        )

    @pytest.mark.asyncio
    async def test_execute_success(self, use_case, mock_repository, session):
        """러닝 세션 종료 성공 테스트"""
        session_id = session.id
        mock_repository.get_by_id.return_value = session
        mock_repository.update.return_value = session

        request = RunningSessionFinishRequestDTO(
            end_location=CoordinateDTO(latitude=37.5680, longitude=126.9790)
        )

        response = await use_case.execute(session_id, request)

        assert response.session_id == session_id
        assert response.finished_at is not None
        mock_repository.get_by_id.assert_called_once_with(session_id)
        mock_repository.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_execute_session_not_found(self, use_case, mock_repository):
        """세션 없음 테스트"""
        session_id = uuid4()
        mock_repository.get_by_id.return_value = None

        request = RunningSessionFinishRequestDTO(
            end_location=CoordinateDTO(latitude=37.5680, longitude=126.9790)
        )

        with pytest.raises(ValueError, match="러닝 세션을 찾을 수 없습니다"):
            await use_case.execute(session_id, request)

