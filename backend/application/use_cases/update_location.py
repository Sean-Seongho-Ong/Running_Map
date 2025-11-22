"""
Update Location Use Case

위치 업데이트 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.exceptions import DatabaseError

from application.dto.running_dto import (
    LocationUpdateRequestDTO,
    LocationUpdateResponseDTO,
)

logger = logging.getLogger(__name__)


class UpdateLocationUseCase:
    """
    위치 업데이트 유즈케이스
    
    러닝 중 현재 위치를 업데이트하고 통계를 계산합니다.
    """

    def __init__(self, running_session_repository: RunningSessionRepository):
        """
        Args:
            running_session_repository: 러닝 세션 리포지토리
        """
        self.running_session_repository = running_session_repository

    async def execute(
        self, session_id: UUID, request: LocationUpdateRequestDTO
    ) -> LocationUpdateResponseDTO:
        """
        위치 업데이트 실행
        
        Args:
            session_id: 러닝 세션 ID
            request: 위치 업데이트 요청
            
        Returns:
            위치 업데이트 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
            ValueError: 세션이 존재하지 않을 때
        """
        try:
            # 1. RunningSessionRepository.get_by_id() 호출
            session = await self.running_session_repository.get_by_id(session_id)

            if session is None:
                raise ValueError(f"러닝 세션을 찾을 수 없습니다 (id={session_id})")

            # 2. RunningSession.add_location() 호출 (새 위치 추가)
            new_location = request.location.to_coordinate()
            session.add_location(new_location, altitude=request.location.altitude)

            # 3. 통계 자동 계산 (거리, 페이스, 속도)
            # 경로를 기반으로 총 거리 계산
            total_distance = session.calculate_total_distance()
            # 경과 시간 계산
            duration = session.get_duration()

            # 통계 업데이트
            session.update_stats(
                distance=total_distance,
                duration=duration,
            )

            # 4. RunningSessionRepository.update() 호출
            updated_session = await self.running_session_repository.update(session)

            logger.info(
                f"위치 업데이트 성공 (id={session_id}, "
                f"distance={total_distance.kilometers:.2f}km, "
                f"duration={duration}s)"
            )

            # 5. LocationUpdateResponse 생성 및 반환
            return LocationUpdateResponseDTO.from_domain(updated_session)

        except ValueError as e:
            logger.error(f"위치 업데이트 실패 - 검증 오류: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"위치 업데이트 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"위치 업데이트 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"위치 업데이트 실패: {str(e)}") from e

