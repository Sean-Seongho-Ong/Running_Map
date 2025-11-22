"""
Running API Tests

러닝 세션 관련 API 엔드포인트 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime, timezone
from starlette.testclient import TestClient

from main import app
import interface.dependencies
from application.dto.running_dto import (
    RunningSessionStartRequestDTO,
    RunningSessionStartResponseDTO,
    RunningSessionUpdateRequestDTO,
    RunningSessionUpdateResponseDTO,
    LocationUpdateRequestDTO,
    LocationUpdateResponseDTO,
    RunningSessionFinishRequestDTO,
    RunningSessionFinishResponseDTO,
    CoordinateDTO,
    LocationDTO,
)


@pytest.fixture
def client():
    """FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    """각 테스트 후 의존성 오버라이드 초기화"""
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def mock_start_running_use_case():
    """Mock StartRunningUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_update_running_use_case():
    """Mock UpdateRunningUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_update_location_use_case():
    """Mock UpdateLocationUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_finish_running_use_case():
    """Mock FinishRunningUseCase"""
    use_case = AsyncMock()
    return use_case


class TestStartRunningAPI:
    """러닝 시작 API 테스트"""

    def test_start_running_success(self, client, mock_start_running_use_case):
        """러닝 시작 성공 테스트"""
        session_id = uuid4()
        response_dto = RunningSessionStartResponseDTO(
            session_id=session_id,
            started_at=datetime.now(timezone.utc),
        )
        mock_start_running_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_start_running_use_case
        ] = lambda: mock_start_running_use_case
        
        request_data = {
            "start_location": {"latitude": 37.5665, "longitude": 126.9780},
        }
        response = client.post("/api/v1/running/start", json=request_data)

        assert response.status_code == 201
        data = response.json()
        assert "session_id" in data


class TestUpdateRunningAPI:
    """러닝 업데이트 API 테스트"""

    def test_update_running_success(self, client, mock_update_running_use_case):
        """러닝 업데이트 성공 테스트"""
        session_id = uuid4()
        from application.dto.running_dto import RunningStatsDTO
        
        response_dto = RunningSessionUpdateResponseDTO(
            session_id=session_id,
            stats=RunningStatsDTO(
                distance=5.0,
                duration=1800,
                pace=6.0,
                speed=10.0,
                elevation_gain=0.0,
                elevation_loss=0.0,
            ),
            route=[
                CoordinateDTO(latitude=37.5665, longitude=126.9780),
                CoordinateDTO(latitude=37.5670, longitude=126.9785),
            ],
        )
        mock_update_running_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_update_running_use_case
        ] = lambda: mock_update_running_use_case
        
        request_data = {
            "stats": {
                "distance": 5.0,
                "duration": 1800,
                "pace": 6.0,
                "speed": 10.0,
                "elevation_gain": 0.0,
                "elevation_loss": 0.0,
            },
        }
        response = client.put(f"/api/v1/running/{session_id}", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == str(session_id)


class TestUpdateLocationAPI:
    """위치 업데이트 API 테스트"""

    def test_update_location_success(self, client, mock_update_location_use_case):
        """위치 업데이트 성공 테스트"""
        session_id = uuid4()
        from application.dto.running_dto import RunningStatsDTO
        
        response_dto = LocationUpdateResponseDTO(
            session_id=session_id,
            stats=RunningStatsDTO(
                distance=0.5,
                duration=300,
                pace=5.0,
                speed=6.0,
                elevation_gain=0.0,
                elevation_loss=0.0,
            ),
            route_length=2,
        )
        mock_update_location_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_update_location_use_case
        ] = lambda: mock_update_location_use_case
        
        request_data = {
            "location": {
                "latitude": 37.5670,
                "longitude": 126.9785,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        response = client.post(
            f"/api/v1/running/{session_id}/location", json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == str(session_id)


class TestFinishRunningAPI:
    """러닝 종료 API 테스트"""

    def test_finish_running_success(self, client, mock_finish_running_use_case):
        """러닝 종료 성공 테스트"""
        session_id = uuid4()
        from application.dto.running_dto import RunningStatsDTO
        
        response_dto = RunningSessionFinishResponseDTO(
            session_id=session_id,
            stats=RunningStatsDTO(
                distance=10.0,
                duration=3600,
                pace=6.0,
                speed=10.0,
                elevation_gain=0.0,
                elevation_loss=0.0,
            ),
            started_at=datetime.now(timezone.utc),
            finished_at=datetime.now(timezone.utc),
            route=[
                CoordinateDTO(latitude=37.5665, longitude=126.9780),
                CoordinateDTO(latitude=37.5670, longitude=126.9785),
            ],
        )
        mock_finish_running_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_finish_running_use_case
        ] = lambda: mock_finish_running_use_case
        
        request_data = {
            "end_location": {"latitude": 37.5680, "longitude": 126.9790},
        }
        response = client.post(
            f"/api/v1/running/{session_id}/finish", json=request_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == str(session_id)
        assert "finished_at" in data

