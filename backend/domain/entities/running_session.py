"""
Running Session Entity

러닝 세션을 나타내는 도메인 엔티티입니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


@dataclass
class RunningStats:
    """러닝 통계 정보"""

    distance: Distance = field(default_factory=lambda: Distance.from_kilometers(0.0))
    duration: int = 0  # 경과 시간 (초)
    pace: float = 0.0  # 평균 페이스 (분/km)
    speed: float = 0.0  # 평균 속도 (km/h)
    elevation_gain: float = 0.0  # 누적 상승 고도 (m)
    elevation_loss: float = 0.0  # 누적 하강 고도 (m)
    current_altitude: Optional[float] = None  # 현재 고도 (m)

    def update_pace(self) -> None:
        """페이스를 계산합니다"""
        if self.distance.kilometers > 0 and self.duration > 0:
            # 페이스 = 시간(분) / 거리(km)
            time_minutes = self.duration / 60.0
            self.pace = time_minutes / self.distance.kilometers
        else:
            self.pace = 0.0

    def update_speed(self) -> None:
        """속도를 계산합니다"""
        if self.duration > 0:
            # 속도 = 거리(km) / 시간(시간)
            time_hours = self.duration / 3600.0
            self.speed = self.distance.kilometers / time_hours if time_hours > 0 else 0.0
        else:
            self.speed = 0.0


@dataclass
class RunningSegment:
    """구간별 통계"""

    index: int
    distance: Distance
    duration: int  # 구간 시간 (초)
    pace: float  # 구간 페이스 (분/km)

    def __post_init__(self):
        """구간 유효성 검증"""
        if self.index < 1:
            raise ValueError("구간 번호는 1 이상이어야 합니다")


@dataclass
class RunningSession:
    """
    러닝 세션 엔티티
    
    Attributes:
        id: 세션 ID (UUID)
        course_id: 사용한 코스 ID (선택사항)
        start_location: 시작 위치
        end_location: 종료 위치 (선택사항)
        route: 러닝 경로 (좌표 배열)
        stats: 러닝 통계
        segments: 구간별 통계 (1km 단위)
        started_at: 시작 시간
        finished_at: 종료 시간 (선택사항)
    """

    start_location: Coordinate
    course_id: Optional[UUID] = None
    end_location: Optional[Coordinate] = None
    route: list[Coordinate] = field(default_factory=list)
    stats: RunningStats = field(default_factory=RunningStats)
    segments: list[RunningSegment] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    finished_at: Optional[datetime] = None

    def __post_init__(self):
        """세션 유효성 검증"""
        if not self.route:
            self.route = [self.start_location]

    def add_location(self, location: Coordinate, altitude: Optional[float] = None) -> None:
        """
        러닝 경로에 위치를 추가합니다.
        
        Args:
            location: 추가할 위치
            altitude: 고도 (선택사항)
        """
        self.route.append(location)
        self.stats.current_altitude = altitude

    def update_stats(
        self,
        distance: Distance,
        duration: int,
        elevation_gain: Optional[float] = None,
        elevation_loss: Optional[float] = None,
    ) -> None:
        """
        러닝 통계를 업데이트합니다.
        
        Args:
            distance: 누적 거리
            duration: 경과 시간 (초)
            elevation_gain: 누적 상승 고도 (m)
            elevation_loss: 누적 하강 고도 (m)
        """
        self.stats.distance = distance
        self.stats.duration = duration
        if elevation_gain is not None:
            self.stats.elevation_gain = elevation_gain
        if elevation_loss is not None:
            self.stats.elevation_loss = elevation_loss

        # 페이스와 속도 자동 계산
        self.stats.update_pace()
        self.stats.update_speed()

    def finish(self, end_location: Coordinate) -> None:
        """
        러닝 세션을 종료합니다.
        
        Args:
            end_location: 종료 위치
        """
        self.end_location = end_location
        self.finished_at = datetime.now(timezone.utc)
        if end_location not in self.route:
            self.route.append(end_location)

    def calculate_total_distance(self) -> Distance:
        """
        경로를 기반으로 총 거리를 계산합니다.
        
        Returns:
            계산된 거리
        """
        if len(self.route) < 2:
            return Distance.from_kilometers(0.0)

        total_distance_km = 0.0
        for i in range(len(self.route) - 1):
            distance_km = self.route[i].distance_to(self.route[i + 1])
            total_distance_km += distance_km

        return Distance.from_kilometers(total_distance_km)

    def get_duration(self) -> int:
        """
        경과 시간을 계산합니다.
        
        Returns:
            경과 시간 (초)
        """
        if self.finished_at:
            return int((self.finished_at - self.started_at).total_seconds())
        else:
            return int((datetime.now(timezone.utc) - self.started_at).total_seconds())

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "course_id": str(self.course_id) if self.course_id else None,
            "start_location": self.start_location.to_dict(),
            "end_location": self.end_location.to_dict() if self.end_location else None,
            "route": [coord.to_dict() for coord in self.route],
            "stats": {
                "distance": self.stats.distance.kilometers,
                "duration": self.stats.duration,
                "pace": self.stats.pace,
                "speed": self.stats.speed,
                "elevation_gain": self.stats.elevation_gain,
                "elevation_loss": self.stats.elevation_loss,
                "current_altitude": self.stats.current_altitude,
            },
            "segments": [
                {
                    "index": seg.index,
                    "distance": seg.distance.kilometers,
                    "duration": seg.duration,
                    "pace": seg.pace,
                }
                for seg in self.segments
            ],
            "started_at": self.started_at.isoformat(),
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
        }

