"""
Delete Course Use Case

코스 삭제 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.course_repository import CourseRepository
from infrastructure.exceptions import DatabaseError

from application.dto.course_dto import CourseDeleteResponseDTO

logger = logging.getLogger(__name__)


class DeleteCourseUseCase:
    """
    코스 삭제 유즈케이스
    
    저장된 코스를 삭제합니다.
    """

    def __init__(self, course_repository: CourseRepository):
        """
        Args:
            course_repository: 코스 리포지토리
        """
        self.course_repository = course_repository

    async def execute(self, course_id: UUID) -> CourseDeleteResponseDTO:
        """
        코스 삭제 실행
        
        Args:
            course_id: 코스 ID
            
        Returns:
            코스 삭제 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
        """
        try:
            # 1. CourseRepository.delete() 호출
            deleted = await self.course_repository.delete(course_id)

            if deleted:
                logger.info(f"코스 삭제 성공 (id={course_id})")
            else:
                logger.warning(f"코스를 찾을 수 없음 (id={course_id})")

            # 2. 삭제 성공 여부를 CourseDeleteResponse로 변환
            return CourseDeleteResponseDTO(
                success=deleted,
                course_id=course_id,
            )

        except DatabaseError as e:
            logger.error(f"코스 삭제 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"코스 삭제 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"코스 삭제 실패: {str(e)}") from e

