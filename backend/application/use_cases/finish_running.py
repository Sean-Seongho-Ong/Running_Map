"""
Finish Running Use Case

러닝 세션 종료 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.exceptions import DatabaseError

from application.dto.running_dto import (
    RunningSessionFinishRequestDTO,
    RunningSessionFinishResponseDTO,
)

logger = logging.getLogger(__name__)


class FinishRunningUseCase:
    """
    러닝 세션 종료 유즈케이스
    
    러닝 세션을 종료하고 최종 통계를 반환합니다.
    """

    def __init__(self, running_session_repository: RunningSessionRepository):
        """
        Args:
            running_session_repository: 러닝 세션 리포지토리
        """
        self.running_session_repository = running_session_repository

    async def execute(
        self, session_id: UUID, request: RunningSessionFinishRequestDTO
    ) -> RunningSessionFinishResponseDTO:
        """
        러닝 세션 종료 실행
        
        Args:
            session_id: 러닝 세션 ID
            request: 러닝 종료 요청
            
        Returns:
            러닝 종료 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
            ValueError: 세션이 존재하지 않을 때
        """
        try:
            # 1. RunningSessionRepository.get_by_id() 호출
            session = await self.running_session_repository.get_by_id(session_id)

            if session is None:
                raise ValueError(f"러닝 세션을 찾을 수 없습니다 (id={session_id})")

            # 2. RunningSession.finish() 호출 (end_location)
            end_location = request.end_location.to_domain()
            session.finish(end_location)

            # 3. 최종 통계 계산
            total_distance = session.calculate_total_distance()
            duration = session.get_duration()

            session.update_stats(
                distance=total_distance,
                duration=duration,
            )

            # 4. RunningSessionRepository.update() 호출
            updated_session = await self.running_session_repository.update(session)

            logger.info(
                f"러닝 세션 종료 성공 (id={session_id}, "
                f"distance={total_distance.kilometers:.2f}km, "
                f"duration={duration}s)"
            )

            # 5. RunningSessionFinishResponse 생성 및 반환
            return RunningSessionFinishResponseDTO.from_domain(updated_session)

        except ValueError as e:
            logger.error(f"러닝 세션 종료 실패 - 검증 오류: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"러닝 세션 종료 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"러닝 세션 종료 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"러닝 세션 종료 실패: {str(e)}") from e

