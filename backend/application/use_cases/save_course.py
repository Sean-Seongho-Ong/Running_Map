"""
Save Course Use Case

코스 저장 유즈케이스입니다.
"""

import logging
from uuid import UUID

from domain.repositories.course_repository import CourseRepository
from infrastructure.exceptions import DatabaseError

from application.dto.course_dto import (
    CourseSaveRequestDTO,
    CourseSaveResponseDTO,
)

logger = logging.getLogger(__name__)


class SaveCourseUseCase:
    """
    코스 저장 유즈케이스
    
    생성된 코스를 데이터베이스에 저장합니다.
    """

    def __init__(self, course_repository: CourseRepository):
        """
        Args:
            course_repository: 코스 리포지토리
        """
        self.course_repository = course_repository

    async def execute(
        self, request: CourseSaveRequestDTO
    ) -> CourseSaveResponseDTO:
        """
        코스 저장 실행
        
        Args:
            request: 코스 저장 요청
            
        Returns:
            코스 저장 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
        """
        try:
            # 1. CourseSaveRequest를 Course 엔티티로 변환
            course = request.to_domain()

            # 2. CourseRepository.create() 호출
            saved_course = await self.course_repository.create(course)

            logger.info(f"코스 저장 성공 (id={saved_course.id}, name={saved_course.name})")

            # 3. 저장된 Course를 CourseSaveResponse로 변환
            return CourseSaveResponseDTO.from_domain(saved_course)

        except DatabaseError as e:
            logger.error(f"코스 저장 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"코스 저장 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"코스 저장 실패: {str(e)}") from e

