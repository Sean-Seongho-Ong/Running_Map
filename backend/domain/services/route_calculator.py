"""
Route Calculator Service Interface

경로 계산을 위한 도메인 서비스 인터페이스입니다.
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class RouteCalculationError(Exception):
    """경로 계산 실패 예외"""

    pass


class RouteCalculator(ABC):
    """
    경로 계산 서비스 인터페이스
    
    두 좌표 간의 경로를 계산합니다.
    """

    @abstractmethod
    async def calculate_route(
        self,
        start: Coordinate,
        end: Coordinate,
        profile: str = "foot",  # foot, bike, car
    ) -> list[Coordinate]:
        """
        두 좌표 간의 경로를 계산합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            profile: 라우팅 프로파일 (foot, bike, car)
            
        Returns:
            경로 좌표 배열
            
        Raises:
            RouteCalculationError: 경로 계산 실패 시
        """
        pass

    @abstractmethod
    async def calculate_distance(
        self,
        start: Coordinate,
        end: Coordinate,
        profile: str = "foot",
    ) -> Distance:
        """
        두 좌표 간의 거리를 계산합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            profile: 라우팅 프로파일 (foot, bike, car)
            
        Returns:
            거리
            
        Raises:
            RouteCalculationError: 거리 계산 실패 시
        """
        pass

