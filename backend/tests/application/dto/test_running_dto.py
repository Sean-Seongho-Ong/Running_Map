"""
Running DTO Tests

Running 관련 DTO의 단위 테스트입니다.
"""

import pytest
from datetime import datetime, timezone
from uuid import uuid4

from application.dto.running_dto import (
    LocationDTO,
    LocationUpdateRequestDTO,
    LocationUpdateResponseDTO,
    RunningSessionFinishRequestDTO,
    RunningSessionFinishResponseDTO,
    RunningSessionStartRequestDTO,
    RunningSessionStartResponseDTO,
    RunningSessionUpdateRequestDTO,
    RunningSessionUpdateResponseDTO,
    RunningStatsDTO,
)
from application.dto.course_dto import CoordinateDTO
from domain.entities.running_session import RunningSession, RunningStats
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class TestLocationDTO:
    """LocationDTO 테스트"""

    def test_create_valid_location(self):
        """유효한 위치 생성 테스트"""
        timestamp = datetime.now(timezone.utc)
        location = LocationDTO(
            latitude=37.5665,
            longitude=126.9780,
            altitude=50.0,
            timestamp=timestamp,
        )
        assert location.latitude == 37.5665
        assert location.altitude == 50.0
        assert location.timestamp == timestamp

    def test_to_coordinate(self):
        """도메인 Coordinate로 변환 테스트"""
        timestamp = datetime.now(timezone.utc)
        location = LocationDTO(
            latitude=37.5665,
            longitude=126.9780,
            timestamp=timestamp,
        )
        coord = location.to_coordinate()
        assert isinstance(coord, Coordinate)
        assert coord.latitude == 37.5665


class TestRunningSessionStartRequestDTO:
    """RunningSessionStartRequestDTO 테스트"""

    def test_create_valid_request(self):
        """유효한 요청 생성 테스트"""
        start_location = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        request = RunningSessionStartRequestDTO(start_location=start_location)
        assert request.start_location.latitude == 37.5665
        assert request.course_id is None

    def test_create_with_course_id(self):
        """코스 ID 포함 요청 생성 테스트"""
        start_location = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        course_id = uuid4()
        request = RunningSessionStartRequestDTO(
            start_location=start_location, course_id=course_id
        )
        assert request.course_id == course_id


class TestRunningSessionStartResponseDTO:
    """RunningSessionStartResponseDTO 테스트"""

    def test_from_domain(self):
        """도메인 RunningSession에서 생성 테스트"""
        start_location = Coordinate(latitude=37.5665, longitude=126.9780)
        session = RunningSession(start_location=start_location)
        response = RunningSessionStartResponseDTO.from_domain(session)
        assert response.session_id == session.id
        assert response.started_at == session.started_at


class TestRunningStatsDTO:
    """RunningStatsDTO 테스트"""

    def test_from_domain(self):
        """도메인 RunningStats에서 생성 테스트"""
        stats = RunningStats(
            distance=Distance.from_kilometers(5.0),
            duration=1800,
            pace=6.0,
            speed=10.0,
        )
        stats_dto = RunningStatsDTO.from_domain(stats)
        assert stats_dto.distance == 5.0
        assert stats_dto.duration == 1800
        assert stats_dto.pace == 6.0
        assert stats_dto.speed == 10.0


class TestRunningSessionUpdateRequestDTO:
    """RunningSessionUpdateRequestDTO 테스트"""

    def test_create_valid_request(self):
        """유효한 요청 생성 테스트"""
        current_location = CoordinateDTO(latitude=37.5670, longitude=126.9785)
        stats = RunningStatsDTO(
            distance=5.0,
            duration=1800,
            pace=6.0,
            speed=10.0,
            elevation_gain=0.0,
            elevation_loss=0.0,
        )
        request = RunningSessionUpdateRequestDTO(
            current_location=current_location, stats=stats
        )
        assert request.current_location is not None
        assert request.stats is not None


class TestLocationUpdateRequestDTO:
    """LocationUpdateRequestDTO 테스트"""

    def test_create_valid_request(self):
        """유효한 요청 생성 테스트"""
        timestamp = datetime.now(timezone.utc)
        location = LocationDTO(
            latitude=37.5670,
            longitude=126.9785,
            timestamp=timestamp,
        )
        request = LocationUpdateRequestDTO(location=location, timestamp=timestamp)
        assert request.location.latitude == 37.5670
        assert request.timestamp == timestamp


class TestRunningSessionFinishRequestDTO:
    """RunningSessionFinishRequestDTO 테스트"""

    def test_create_valid_request(self):
        """유효한 요청 생성 테스트"""
        end_location = CoordinateDTO(latitude=37.5680, longitude=126.9790)
        request = RunningSessionFinishRequestDTO(end_location=end_location)
        assert request.end_location.latitude == 37.5680


class TestRunningSessionFinishResponseDTO:
    """RunningSessionFinishResponseDTO 테스트"""

    def test_from_domain(self):
        """도메인 RunningSession에서 생성 테스트"""
        start_location = Coordinate(latitude=37.5665, longitude=126.9780)
        end_location = Coordinate(latitude=37.5680, longitude=126.9790)
        session = RunningSession(start_location=start_location)
        session.finish(end_location)
        response = RunningSessionFinishResponseDTO.from_domain(session)
        assert response.session_id == session.id
        assert response.finished_at is not None
        assert len(response.route) > 0

