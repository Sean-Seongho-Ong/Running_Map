"""
Coordinate Value Object

WGS84 좌표계의 위도/경도를 나타내는 불변 값 객체입니다.
Haversine 공식을 사용하여 거리를 계산합니다.
"""

import math
from typing import Self
from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinate:
    """
    좌표 값 객체 (WGS84)
    
    Attributes:
        latitude: 위도 (-90 ~ 90)
        longitude: 경도 (-180 ~ 180)
    """

    latitude: float
    longitude: float

    def __post_init__(self):
        """좌표 유효성 검증"""
        if not (-90 <= self.latitude <= 90):
            raise ValueError(
                f"위도는 -90과 90 사이여야 합니다. 현재 값: {self.latitude}"
            )
        if not (-180 <= self.longitude <= 180):
            raise ValueError(
                f"경도는 -180과 180 사이여야 합니다. 현재 값: {self.longitude}"
            )

    def distance_to(self, other: Self) -> float:
        """
        다른 좌표까지의 거리를 계산합니다 (Haversine 공식).
        
        Args:
            other: 대상 좌표
            
        Returns:
            거리 (킬로미터)
        """
        # 지구 반지름 (km)
        EARTH_RADIUS_KM = 6371.0

        # 위도와 경도를 라디안으로 변환
        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(other.latitude)
        lon2_rad = math.radians(other.longitude)

        # 위도와 경도의 차이
        delta_lat = lat2_rad - lat1_rad
        delta_lon = lon2_rad - lon1_rad

        # Haversine 공식
        a = (
            math.sin(delta_lat / 2) ** 2
            + math.cos(lat1_rad)
            * math.cos(lat2_rad)
            * math.sin(delta_lon / 2) ** 2
        )
        c = 2 * math.asin(math.sqrt(a))

        # 거리 계산
        distance_km = EARTH_RADIUS_KM * c

        return distance_km

    def bearing_to(self, other: Self) -> float:
        """
        다른 좌표까지의 방위각을 계산합니다.
        
        Args:
            other: 대상 좌표
            
        Returns:
            방위각 (도, 0~360)
        """
        lat1_rad = math.radians(self.latitude)
        lon1_rad = math.radians(self.longitude)
        lat2_rad = math.radians(other.latitude)
        lon2_rad = math.radians(other.longitude)

        delta_lon = lon2_rad - lon1_rad

        y = math.sin(delta_lon) * math.cos(lat2_rad)
        x = (
            math.cos(lat1_rad) * math.sin(lat2_rad)
            - math.sin(lat1_rad)
            * math.cos(lat2_rad)
            * math.cos(delta_lon)
        )

        bearing_rad = math.atan2(y, x)
        bearing_deg = math.degrees(bearing_rad)

        # 0~360 범위로 정규화
        return (bearing_deg + 360) % 360

    def to_dict(self) -> dict[str, float]:
        """딕셔너리로 변환"""
        return {"latitude": self.latitude, "longitude": self.longitude}

    @classmethod
    def from_dict(cls, data: dict[str, float]) -> Self:
        """딕셔너리에서 생성"""
        return cls(
            latitude=data["latitude"],
            longitude=data["longitude"],
        )

    def __str__(self) -> str:
        return f"Coordinate(lat={self.latitude}, lon={self.longitude})"

    def __repr__(self) -> str:
        return self.__str__()

