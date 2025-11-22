"""
Pytest Configuration

테스트 공통 설정 및 픽스처입니다.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from domain.entities.course import Course, CourseMetadata
from domain.entities.running_session import RunningSession, RunningStats
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


@pytest.fixture
def sample_coordinate():
    """샘플 좌표"""
    return Coordinate(latitude=37.5665, longitude=126.9780)


@pytest.fixture
def sample_distance():
    """샘플 거리"""
    return Distance.from_kilometers(10.0)


@pytest.fixture
def sample_course(sample_coordinate, sample_distance):
    """샘플 코스"""
    polyline = [
        sample_coordinate,
        Coordinate(latitude=37.5670, longitude=126.9785),
        Coordinate(latitude=37.5675, longitude=126.9790),
    ]
    return Course(
        name="테스트 코스",
        polyline=polyline,
        distance=sample_distance,
        metadata=CourseMetadata(),
    )


@pytest.fixture
def sample_running_session(sample_coordinate):
    """샘플 러닝 세션"""
    return RunningSession(
        start_location=sample_coordinate,
        route=[sample_coordinate],
        stats=RunningStats(),
    )


@pytest.fixture
def mock_db_session():
    """Mock 데이터베이스 세션"""
    session = AsyncMock()
    return session


@pytest.fixture
def mock_redis_client():
    """Mock Redis 클라이언트"""
    client = AsyncMock()
    client.ping = AsyncMock(return_value=True)
    client.get = AsyncMock(return_value=None)
    client.set = AsyncMock(return_value=True)
    client.setex = AsyncMock(return_value=True)
    client.delete = AsyncMock(return_value=1)
    client.exists = AsyncMock(return_value=0)
    client.scan_iter = AsyncMock(return_value=iter([]))
    return client

