"""
Distance Calculator Service Interface

거리 계산을 위한 도메인 서비스 인터페이스입니다.
"""

from abc import ABC, abstractmethod

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class DistanceCalculator(ABC):
    """
    거리 계산 서비스 인터페이스
    
    좌표 간의 거리를 계산합니다.
    """

    @abstractmethod
    def calculate_distance(
        self,
        start: Coordinate,
        end: Coordinate,
    ) -> Distance:
        """
        두 좌표 간의 거리를 계산합니다 (직선 거리).
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            
        Returns:
            거리
        """
        pass

    @abstractmethod
    def calculate_total_distance(
        self,
        coordinates: list[Coordinate],
    ) -> Distance:
        """
        좌표 배열의 총 거리를 계산합니다.
        
        Args:
            coordinates: 좌표 배열
            
        Returns:
            총 거리
        """
        pass


class HaversineDistanceCalculator(DistanceCalculator):
    """
    Haversine 공식을 사용한 거리 계산 구현
    
    직선 거리를 계산합니다.
    """

    def calculate_distance(
        self,
        start: Coordinate,
        end: Coordinate,
    ) -> Distance:
        """두 좌표 간의 직선 거리를 계산합니다"""
        distance_km = start.distance_to(end)
        return Distance.from_kilometers(distance_km)

    def calculate_total_distance(
        self,
        coordinates: list[Coordinate],
    ) -> Distance:
        """좌표 배열의 총 직선 거리를 계산합니다"""
        if len(coordinates) < 2:
            return Distance.from_kilometers(0.0)

        total_distance_km = 0.0
        for i in range(len(coordinates) - 1):
            distance_km = coordinates[i].distance_to(coordinates[i + 1])
            total_distance_km += distance_km

        return Distance.from_kilometers(total_distance_km)
