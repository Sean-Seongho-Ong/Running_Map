"""
Mock Loop Generator

테스트 및 개발용 Mock LoopGenerator 구현체입니다.
실제 알고리즘 구현 전까지 사용합니다.
"""

from domain.entities.route import Route
from domain.services.loop_generator import LoopGenerator, LoopGenerationError
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class MockLoopGenerator(LoopGenerator):
    """테스트 및 개발용 Mock LoopGenerator"""

    def __init__(self, should_fail: bool = False):
        """
        Args:
            should_fail: True이면 LoopGenerationError 발생
        """
        self.should_fail = should_fail

    async def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: dict | None = None,
    ) -> Route:
        """
        Mock 루프 생성
        
        간단한 더미 루프를 생성합니다.
        """
        if self.should_fail:
            raise LoopGenerationError("루프 생성 실패")

        # 간단한 더미 루프 생성 (사각형 형태)
        polyline = [
            start_point,
            Coordinate(
                latitude=start_point.latitude + 0.01,
                longitude=start_point.longitude,
            ),
            Coordinate(
                latitude=start_point.latitude + 0.01,
                longitude=start_point.longitude + 0.01,
            ),
            Coordinate(
                latitude=start_point.latitude,
                longitude=start_point.longitude + 0.01,
            ),
            start_point,  # 루프 닫기
        ]

        # 실제 거리는 target_distance와 약간 다를 수 있음
        actual_distance = target_distance

        return Route(
            polyline=polyline,
            distance=actual_distance,
            algorithm="STEP_ADAPTIVE",
            iterations=3,
            step_used=1.0,
            relative_error=0.05,  # 5% 오차
        )

