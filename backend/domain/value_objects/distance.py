"""
Distance Value Object

거리를 나타내는 불변 값 객체입니다.
킬로미터와 미터 단위를 지원하며, 오차 처리를 포함합니다.
"""

from typing import Self
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Distance:
    """
    거리 값 객체
    
    Attributes:
        kilometers: 거리 (킬로미터)
    """

    kilometers: float

    def __post_init__(self):
        """거리 유효성 검증"""
        if self.kilometers < 0:
            raise ValueError(
                f"거리는 0 이상이어야 합니다. 현재 값: {self.kilometers}"
            )
        if not math.isfinite(self.kilometers):
            raise ValueError(f"거리는 유한한 값이어야 합니다. 현재 값: {self.kilometers}")

    @property
    def meters(self) -> float:
        """미터 단위로 변환"""
        return self.kilometers * 1000.0

    @classmethod
    def from_kilometers(cls, km: float) -> Self:
        """킬로미터로부터 생성"""
        return cls(kilometers=km)

    @classmethod
    def from_meters(cls, m: float) -> Self:
        """미터로부터 생성"""
        return cls(kilometers=m / 1000.0)

    def add(self, other: Self) -> Self:
        """다른 거리를 더합니다"""
        return Distance(kilometers=self.kilometers + other.kilometers)

    def subtract(self, other: Self) -> Self:
        """다른 거리를 뺍니다"""
        result = self.kilometers - other.kilometers
        if result < 0:
            raise ValueError("거리는 음수가 될 수 없습니다")
        return Distance(kilometers=result)

    def multiply(self, factor: float) -> Self:
        """거리에 배수를 곱합니다"""
        if factor < 0:
            raise ValueError("배수는 0 이상이어야 합니다")
        return Distance(kilometers=self.kilometers * factor)

    def divide(self, divisor: float) -> Self:
        """거리를 나눕니다"""
        if divisor == 0:
            raise ValueError("0으로 나눌 수 없습니다")
        if divisor < 0:
            raise ValueError("제수는 0보다 커야 합니다")
        return Distance(kilometers=self.kilometers / divisor)

    def relative_error(self, target: Self) -> float:
        """
        목표 거리 대비 상대 오차를 계산합니다.
        
        Args:
            target: 목표 거리
            
        Returns:
            상대 오차 (|L - D| / D)
        """
        if target.kilometers == 0:
            raise ValueError("목표 거리는 0이 될 수 없습니다")
        return abs(self.kilometers - target.kilometers) / target.kilometers

    def absolute_error(self, target: Self) -> Self:
        """
        목표 거리 대비 절대 오차를 계산합니다.
        
        Args:
            target: 목표 거리
            
        Returns:
            절대 오차 (|L - D|)
        """
        return Distance(kilometers=abs(self.kilometers - target.kilometers))

    def is_within_tolerance(
        self, target: Self, tolerance_ratio: float
    ) -> bool:
        """
        목표 거리 대비 허용 오차 범위 내에 있는지 확인합니다.
        
        Args:
            target: 목표 거리
            tolerance_ratio: 허용 오차 비율 (0.0 ~ 1.0)
            
        Returns:
            허용 오차 범위 내이면 True
        """
        if tolerance_ratio < 0 or tolerance_ratio > 1:
            raise ValueError("허용 오차 비율은 0.0과 1.0 사이여야 합니다")
        return self.relative_error(target) <= tolerance_ratio

    def __lt__(self, other: Self) -> bool:
        """작다 비교"""
        return self.kilometers < other.kilometers

    def __le__(self, other: Self) -> bool:
        """작거나 같다 비교"""
        return self.kilometers <= other.kilometers

    def __gt__(self, other: Self) -> bool:
        """크다 비교"""
        return self.kilometers > other.kilometers

    def __ge__(self, other: Self) -> bool:
        """크거나 같다 비교"""
        return self.kilometers >= other.kilometers

    def __str__(self) -> str:
        return f"Distance({self.kilometers:.2f} km)"

    def __repr__(self) -> str:
        return self.__str__()

