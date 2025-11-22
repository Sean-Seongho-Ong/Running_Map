"""
Get Course Use Case

코스 상세 조회 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.course_repository import CourseRepository
from infrastructure.exceptions import DatabaseError

from application.dto.course_dto import CourseDetailResponseDTO

logger = logging.getLogger(__name__)


class GetCourseUseCase:
    """
    코스 상세 조회 유즈케이스
    
    저장된 코스의 상세 정보를 조회합니다.
    """

    def __init__(self, course_repository: CourseRepository):
        """
        Args:
            course_repository: 코스 리포지토리
        """
        self.course_repository = course_repository

    async def execute(self, course_id: UUID) -> CourseDetailResponseDTO | None:
        """
        코스 상세 조회 실행
        
        Args:
            course_id: 코스 ID
            
        Returns:
            코스 상세 응답 (코스가 없으면 None)
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
        """
        try:
            # 1. CourseRepository.get_by_id() 호출
            course = await self.course_repository.get_by_id(course_id)

            if course is None:
                logger.warning(f"코스를 찾을 수 없음 (id={course_id})")
                return None

            logger.info(f"코스 상세 조회 성공 (id={course_id})")

            # 2. Course 엔티티를 CourseDetailResponse로 변환
            return CourseDetailResponseDTO.from_domain(course)

        except DatabaseError as e:
            logger.error(f"코스 상세 조회 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"코스 상세 조회 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"코스 상세 조회 실패: {str(e)}") from e

