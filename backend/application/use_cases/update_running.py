"""
Update Running Use Case

러닝 세션 업데이트 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.exceptions import DatabaseError

from application.dto.running_dto import (
    RunningSessionUpdateRequestDTO,
    RunningSessionUpdateResponseDTO,
)

logger = logging.getLogger(__name__)


class UpdateRunningUseCase:
    """
    러닝 세션 업데이트 유즈케이스
    
    러닝 세션의 현재 상태를 업데이트합니다.
    """

    def __init__(self, running_session_repository: RunningSessionRepository):
        """
        Args:
            running_session_repository: 러닝 세션 리포지토리
        """
        self.running_session_repository = running_session_repository

    async def execute(
        self, session_id: UUID, request: RunningSessionUpdateRequestDTO
    ) -> RunningSessionUpdateResponseDTO:
        """
        러닝 세션 업데이트 실행
        
        Args:
            session_id: 러닝 세션 ID
            request: 러닝 업데이트 요청
            
        Returns:
            러닝 업데이트 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
            ValueError: 세션이 존재하지 않을 때
        """
        try:
            # 1. RunningSessionRepository.get_by_id() 호출
            session = await self.running_session_repository.get_by_id(session_id)

            if session is None:
                raise ValueError(f"러닝 세션을 찾을 수 없습니다 (id={session_id})")

            # 2. RunningSession 엔티티 업데이트
            if request.current_location:
                session.add_location(request.current_location.to_domain())

            if request.stats:
                session.update_stats(
                    distance=Distance.from_kilometers(request.stats.distance),
                    duration=request.stats.duration,
                    elevation_gain=request.stats.elevation_gain,
                    elevation_loss=request.stats.elevation_loss,
                )

            # 3. RunningSessionRepository.update() 호출
            updated_session = await self.running_session_repository.update(session)

            logger.info(f"러닝 세션 업데이트 성공 (id={session_id})")

            # 4. RunningSessionUpdateResponse 생성 및 반환
            return RunningSessionUpdateResponseDTO.from_domain(updated_session)

        except ValueError as e:
            logger.error(f"러닝 세션 업데이트 실패 - 검증 오류: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"러닝 세션 업데이트 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"러닝 세션 업데이트 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"러닝 세션 업데이트 실패: {str(e)}") from e

