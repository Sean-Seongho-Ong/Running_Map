"""
Running DTOs

러닝 세션 관련 데이터 전송 객체입니다.
OpenAPI 명세서를 기반으로 정의됩니다.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from application.dto.course_dto import CoordinateDTO
from domain.entities.running_session import RunningSession, RunningStats
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class LocationDTO(BaseModel):
    """위치 정보 DTO (좌표 + 고도 + 타임스탬프)"""

    latitude: float = Field(..., ge=-90, le=90, description="위도 (WGS84)")
    longitude: float = Field(..., ge=-180, le=180, description="경도 (WGS84)")
    altitude: Optional[float] = Field(default=None, description="고도 (미터)")
    timestamp: datetime = Field(..., description="위치 수집 시각 (ISO 8601)")

    def to_coordinate(self) -> Coordinate:
        """도메인 Coordinate로 변환"""
        return Coordinate(latitude=self.latitude, longitude=self.longitude)

    @classmethod
    def from_coordinate(cls, coordinate: Coordinate, timestamp: datetime, altitude: Optional[float] = None) -> "LocationDTO":
        """도메인 Coordinate에서 생성"""
        return cls(
            latitude=coordinate.latitude,
            longitude=coordinate.longitude,
            altitude=altitude,
            timestamp=timestamp,
        )


class RunningSessionStartRequestDTO(BaseModel):
    """러닝 세션 시작 요청 DTO"""

    start_location: CoordinateDTO = Field(..., description="시작 위치")
    course_id: Optional[UUID] = Field(default=None, description="사용할 코스 ID (선택사항)")


class RunningSessionStartResponseDTO(BaseModel):
    """러닝 세션 시작 응답 DTO"""

    session_id: UUID = Field(..., description="러닝 세션 ID")
    started_at: datetime = Field(..., description="시작 시간")

    @classmethod
    def from_domain(cls, session: RunningSession) -> "RunningSessionStartResponseDTO":
        """도메인 RunningSession에서 생성"""
        return cls(
            session_id=session.id,
            started_at=session.started_at,
        )


class RunningStatsDTO(BaseModel):
    """러닝 통계 DTO"""

    distance: float = Field(..., ge=0, description="누적 거리 (km)")
    duration: int = Field(..., ge=0, description="경과 시간 (초)")
    pace: float = Field(..., ge=0, description="평균 페이스 (분/km)")
    speed: float = Field(..., ge=0, description="평균 속도 (km/h)")
    elevation_gain: float = Field(..., ge=0, description="누적 상승 고도 (m)")
    elevation_loss: float = Field(..., ge=0, description="누적 하강 고도 (m)")
    current_altitude: Optional[float] = Field(default=None, description="현재 고도 (m)")

    @classmethod
    def from_domain(cls, stats: RunningStats) -> "RunningStatsDTO":
        """도메인 RunningStats에서 생성"""
        return cls(
            distance=stats.distance.kilometers,
            duration=stats.duration,
            pace=stats.pace,
            speed=stats.speed,
            elevation_gain=stats.elevation_gain,
            elevation_loss=stats.elevation_loss,
            current_altitude=stats.current_altitude,
        )


class RunningSessionUpdateRequestDTO(BaseModel):
    """러닝 세션 업데이트 요청 DTO"""

    current_location: Optional[CoordinateDTO] = Field(default=None, description="현재 위치")
    stats: Optional[RunningStatsDTO] = Field(default=None, description="러닝 통계")


class RunningSessionUpdateResponseDTO(BaseModel):
    """러닝 세션 업데이트 응답 DTO"""

    session_id: UUID = Field(..., description="러닝 세션 ID")
    stats: RunningStatsDTO = Field(..., description="업데이트된 러닝 통계")
    route: list[CoordinateDTO] = Field(..., description="러닝 경로")

    @classmethod
    def from_domain(cls, session: RunningSession) -> "RunningSessionUpdateResponseDTO":
        """도메인 RunningSession에서 생성"""
        return cls(
            session_id=session.id,
            stats=RunningStatsDTO.from_domain(session.stats),
            route=[CoordinateDTO.from_domain(coord) for coord in session.route],
        )


class LocationUpdateRequestDTO(BaseModel):
    """위치 업데이트 요청 DTO"""

    location: LocationDTO = Field(..., description="현재 위치 정보")
    timestamp: datetime = Field(..., description="위치 수집 시각")


class LocationUpdateResponseDTO(BaseModel):
    """위치 업데이트 응답 DTO"""

    session_id: UUID = Field(..., description="러닝 세션 ID")
    stats: RunningStatsDTO = Field(..., description="업데이트된 러닝 통계")
    route_length: int = Field(..., description="경로 좌표 개수")

    @classmethod
    def from_domain(cls, session: RunningSession) -> "LocationUpdateResponseDTO":
        """도메인 RunningSession에서 생성"""
        return cls(
            session_id=session.id,
            stats=RunningStatsDTO.from_domain(session.stats),
            route_length=len(session.route),
        )


class RunningSessionFinishRequestDTO(BaseModel):
    """러닝 세션 종료 요청 DTO"""

    end_location: CoordinateDTO = Field(..., description="종료 위치")


class RunningSessionFinishResponseDTO(BaseModel):
    """러닝 세션 종료 응답 DTO"""

    session_id: UUID = Field(..., description="러닝 세션 ID")
    stats: RunningStatsDTO = Field(..., description="최종 러닝 통계")
    started_at: datetime = Field(..., description="시작 시간")
    finished_at: datetime = Field(..., description="종료 시간")
    route: list[CoordinateDTO] = Field(..., description="러닝 경로")

    @classmethod
    def from_domain(cls, session: RunningSession) -> "RunningSessionFinishResponseDTO":
        """도메인 RunningSession에서 생성"""
        return cls(
            session_id=session.id,
            stats=RunningStatsDTO.from_domain(session.stats),
            started_at=session.started_at,
            finished_at=session.finished_at or datetime.now(),
            route=[CoordinateDTO.from_domain(coord) for coord in session.route],
        )

