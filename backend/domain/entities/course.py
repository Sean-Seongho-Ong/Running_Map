"""
Course Entity

러닝 코스를 나타내는 도메인 엔티티입니다.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


@dataclass
class CourseMetadata:
    """코스 메타데이터"""

    estimated_time: Optional[int] = None  # 예상 소요 시간 (분)
    elevation_gain: Optional[float] = None  # 누적 상승 고도 (m)
    elevation_loss: Optional[float] = None  # 누적 하강 고도 (m)
    quality_score: Optional[float] = None  # 코스 품질 점수 (0.0 ~ 1.0)
    self_intersections: Optional[int] = None  # 자기 교차 횟수
    tags: list[str] = field(default_factory=list)  # 코스 태그
    difficulty: Optional[str] = None  # 난이도 (easy, medium, hard)

    def __post_init__(self):
        """메타데이터 유효성 검증"""
        if self.quality_score is not None:
            if not (0.0 <= self.quality_score <= 1.0):
                raise ValueError(
                    f"품질 점수는 0.0과 1.0 사이여야 합니다. 현재 값: {self.quality_score}"
                )
        if self.difficulty is not None:
            if self.difficulty not in ["easy", "medium", "hard"]:
                raise ValueError(
                    f"난이도는 easy, medium, hard 중 하나여야 합니다. 현재 값: {self.difficulty}"
                )


@dataclass
class Course:
    """
    코스 엔티티
    
    Attributes:
        id: 코스 ID (UUID)
        name: 코스 이름
        polyline: 폴리라인 좌표 배열
        distance: 코스 거리
        metadata: 코스 메타데이터
        is_public: 공개 여부
        user_id: 사용자 ID (향후 구현)
        created_at: 생성일시
        updated_at: 수정일시
    """

    name: str
    polyline: list[Coordinate]
    distance: Distance
    metadata: CourseMetadata = field(default_factory=CourseMetadata)
    is_public: bool = False
    user_id: Optional[UUID] = None
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """코스 유효성 검증"""
        if not self.name or not self.name.strip():
            raise ValueError("코스 이름은 필수입니다")
        if len(self.polyline) < 2:
            raise ValueError("폴리라인은 최소 2개 이상의 좌표가 필요합니다")
        if self.distance.kilometers <= 0:
            raise ValueError("코스 거리는 0보다 커야 합니다")

    def calculate_actual_distance(self) -> Distance:
        """
        폴리라인을 기반으로 실제 거리를 계산합니다.
        
        Returns:
            계산된 거리
        """
        if len(self.polyline) < 2:
            return Distance.from_kilometers(0.0)

        total_distance_km = 0.0
        for i in range(len(self.polyline) - 1):
            distance_km = self.polyline[i].distance_to(self.polyline[i + 1])
            total_distance_km += distance_km

        return Distance.from_kilometers(total_distance_km)

    def update_name(self, new_name: str) -> None:
        """코스 이름을 업데이트합니다"""
        if not new_name or not new_name.strip():
            raise ValueError("코스 이름은 필수입니다")
        self.name = new_name.strip()
        self.updated_at = datetime.now(timezone.utc)

    def update_metadata(self, metadata: CourseMetadata) -> None:
        """코스 메타데이터를 업데이트합니다"""
        self.metadata = metadata
        self.updated_at = datetime.now(timezone.utc)

    def set_public(self, is_public: bool) -> None:
        """공개 여부를 설정합니다"""
        self.is_public = is_public
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "id": str(self.id),
            "name": self.name,
            "polyline": [coord.to_dict() for coord in self.polyline],
            "distance": self.distance.kilometers,
            "metadata": {
                "estimated_time": self.metadata.estimated_time,
                "elevation_gain": self.metadata.elevation_gain,
                "elevation_loss": self.metadata.elevation_loss,
                "quality_score": self.metadata.quality_score,
                "self_intersections": self.metadata.self_intersections,
                "tags": self.metadata.tags,
                "difficulty": self.metadata.difficulty,
            },
            "is_public": self.is_public,
            "user_id": str(self.user_id) if self.user_id else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

