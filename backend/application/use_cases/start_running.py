"""
Start Running Use Case

러닝 세션 시작 유즈케이스입니다.
"""

import logging
from typing import Optional
from uuid import UUID

from domain.entities.running_session import RunningSession
from domain.repositories.course_repository import CourseRepository
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate
from infrastructure.exceptions import DatabaseError

from application.dto.running_dto import (
    RunningSessionStartRequestDTO,
    RunningSessionStartResponseDTO,
)

logger = logging.getLogger(__name__)


class StartRunningUseCase:
    """
    러닝 세션 시작 유즈케이스
    
    새로운 러닝 세션을 시작합니다.
    """

    def __init__(
        self,
        running_session_repository: RunningSessionRepository,
        course_repository: Optional[CourseRepository] = None,
    ):
        """
        Args:
            running_session_repository: 러닝 세션 리포지토리
            course_repository: 코스 리포지토리 (선택사항, course_id 검증용)
        """
        self.running_session_repository = running_session_repository
        self.course_repository = course_repository

    async def execute(
        self, request: RunningSessionStartRequestDTO
    ) -> RunningSessionStartResponseDTO:
        """
        러닝 세션 시작 실행
        
        Args:
            request: 러닝 시작 요청
            
        Returns:
            러닝 시작 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
            ValueError: 코스가 존재하지 않을 때
        """
        try:
            # 1. RunningSession 엔티티 생성
            start_location = request.start_location.to_domain()
            session = RunningSession(
                start_location=start_location,
                course_id=request.course_id,
            )

            # 2. course_id가 있으면 Course 존재 확인
            if request.course_id and self.course_repository:
                course = await self.course_repository.get_by_id(request.course_id)
                if course is None:
                    raise ValueError(f"코스를 찾을 수 없습니다 (id={request.course_id})")

            # 3. RunningSessionRepository.create() 호출
            created_session = await self.running_session_repository.create(session)

            logger.info(
                f"러닝 세션 시작 성공 (id={created_session.id}, "
                f"course_id={request.course_id})"
            )

            # 4. RunningSessionStartResponse 생성 및 반환
            return RunningSessionStartResponseDTO.from_domain(created_session)

        except ValueError as e:
            logger.error(f"러닝 세션 시작 실패 - 검증 오류: {e}")
            raise
        except DatabaseError as e:
            logger.error(f"러닝 세션 시작 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"러닝 세션 시작 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"러닝 세션 시작 실패: {str(e)}") from e

