"""
Generate Course Use Case

코스 생성 유즈케이스입니다.
"""

import logging
from typing import Optional

from domain.entities.route import Route
from domain.services.loop_generator import LoopGenerator, LoopGenerationError
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

from application.dto.course_dto import (
    CourseGenerationRequestDTO,
    CourseGenerationResponseDTO,
    CourseGenerationResultDTO,
    CourseMetadataDTO,
)
from infrastructure.cache.course_cache import CourseCacheService

logger = logging.getLogger(__name__)


class GenerateCourseUseCase:
    """
    코스 생성 유즈케이스
    
    사용자 위치와 목표 거리를 기반으로 Distance-Constrained Loop Generation Algorithm을 사용하여
    러닝 코스를 자동 생성합니다.
    """

    def __init__(
        self,
        loop_generator: LoopGenerator,
    ):
        """
        Args:
            loop_generator: 루프 생성 알고리즘 구현체
        """
        self.loop_generator = loop_generator

    async def execute(
        self, request: CourseGenerationRequestDTO
    ) -> CourseGenerationResponseDTO:
        """
        코스 생성 실행
        
        Args:
            request: 코스 생성 요청
            
        Returns:
            코스 생성 응답
            
        Raises:
            LoopGenerationError: 루프 생성 실패 시
        """
        try:
            # 1. 캐시 확인 (동일 시작점 + 거리)
            cached_result = await CourseCacheService.get_course(
                request.start_point.latitude,
                request.start_point.longitude,
                request.target_distance,
            )

            if cached_result:
                logger.info(
                    f"코스 캐시 히트 (lat={request.start_point.latitude}, "
                    f"lon={request.start_point.longitude}, distance={request.target_distance})"
                )
                # 캐시된 결과를 응답으로 변환
                return CourseGenerationResponseDTO(
                    status="OK",
                    course=CourseGenerationResultDTO(**cached_result),
                )

            # 2. 루프 생성 알고리즘 실행
            start_point = request.start_point.to_domain()
            target_distance = Distance.from_kilometers(request.target_distance)
            parameters = (
                request.parameters.model_dump() if request.parameters else None
            )

            route = await self.loop_generator.generate(
                start_point=start_point,
                target_distance=target_distance,
                parameters=parameters,
            )

            # 3. 상대 오차 계산 (아직 계산되지 않은 경우)
            if route.relative_error == 0.0:
                actual_distance = route.distance.kilometers
                target_distance_km = target_distance.kilometers
                if target_distance_km > 0:
                    route.relative_error = abs(
                        actual_distance - target_distance_km
                    ) / target_distance_km
                else:
                    route.relative_error = 0.0

            # 4. 결과를 캐시에 저장 (TTL: 24시간)
            course_result = CourseGenerationResultDTO.from_route(route)
            cache_data = course_result.model_dump()
            await CourseCacheService.set_course(
                request.start_point.latitude,
                request.start_point.longitude,
                request.target_distance,
                cache_data,
            )

            logger.info(
                f"코스 생성 성공 (algorithm={route.algorithm}, "
                f"distance={route.distance.kilometers:.2f}km, "
                f"relative_error={route.relative_error:.3f})"
            )

            # 5. 응답 생성
            return CourseGenerationResponseDTO(
                status="OK",
                course=course_result,
            )

        except LoopGenerationError as e:
            logger.error(f"코스 생성 실패: {e}")
            return CourseGenerationResponseDTO(
                status="FAIL",
                course=None,
                error={
                    "code": "COURSE_GENERATION_FAILED",
                    "message": str(e),
                },
            )
        except Exception as e:
            logger.error(f"코스 생성 중 예상치 못한 오류: {e}", exc_info=True)
            return CourseGenerationResponseDTO(
                status="FAIL",
                course=None,
                error={
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "코스 생성 중 오류가 발생했습니다.",
                },
            )

