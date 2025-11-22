"""
Loop Generator Service Interface

루프 생성 알고리즘을 위한 도메인 서비스 인터페이스입니다.
"""

from abc import ABC, abstractmethod
from typing import Optional

from domain.entities.route import Route
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class LoopGenerationError(Exception):
    """루프 생성 실패 예외"""

    pass


class LoopGenerator(ABC):
    """
    루프 생성 알고리즘 인터페이스
    
    Distance-Constrained Loop Generation Algorithm v1.0을 구현합니다.
    """

    @abstractmethod
    async def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: Optional[dict] = None,
    ) -> Route:
        """
        루프 생성
        
        Args:
            start_point: 시작점 좌표
            target_distance: 목표 거리
            parameters: 알고리즘 파라미터
                - step_init: 초기 스텝 길이 (기본값: 1.0 km)
                - step_min: 최소 스텝 길이 (기본값: 0.4 km)
                - step_max: 최대 스텝 길이 (기본값: 2.0 km)
                - tolerance_ratio: 허용 오차 비율 (기본값: 0.1)
                - shrink_factor: Step 축소 계수 (기본값: 0.8)
                - grow_factor: Step 확대 계수 (기본값: 1.2)
                - max_iter: 최대 반복 횟수 (기본값: 5)
                - use_SP_fallback: S-P 기반 Fallback 사용 여부 (기본값: True)
        
        Returns:
            Route: 생성된 루프 경로
            
        Raises:
            LoopGenerationError: 루프 생성 실패 시
        """
        pass

