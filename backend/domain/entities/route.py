"""
Route Entity

경로를 나타내는 도메인 엔티티입니다.
코스 생성 알고리즘의 결과로 사용됩니다.
"""

from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


@dataclass
class Route:
    """
    경로 엔티티
    
    Attributes:
        id: 경로 ID (UUID)
        polyline: 폴리라인 좌표 배열
        distance: 경로 거리
        algorithm: 사용된 알고리즘
        iterations: 반복 횟수
        step_used: 사용된 step 값 (선택사항)
    """

    polyline: list[Coordinate]
    distance: Distance
    algorithm: str  # STEP_ADAPTIVE, SP_BASED, FALLBACK
    iterations: int = 0
    step_used: Optional[float] = None
    relative_error: float = 0.0  # 상대 오차 (|L - D| / D)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        """경로 유효성 검증"""
        if len(self.polyline) < 2:
            raise ValueError("경로는 최소 2개 이상의 좌표가 필요합니다")
        if self.distance.kilometers <= 0:
            raise ValueError("경로 거리는 0보다 커야 합니다")
        if self.algorithm not in ["STEP_ADAPTIVE", "SP_BASED", "FALLBACK"]:
            raise ValueError(
                f"알고리즘은 STEP_ADAPTIVE, SP_BASED, FALLBACK 중 하나여야 합니다. 현재 값: {self.algorithm}"
            )

