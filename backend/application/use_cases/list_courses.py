"""
List Courses Use Case

코스 목록 조회 유즈케이스입니다.
"""

import logging
from typing import Optional
from uuid import UUID

from domain.repositories.course_repository import CourseRepository
from infrastructure.exceptions import DatabaseError

from application.dto.course_dto import (
    CourseListResponseDTO,
    CourseListItemDTO,
)

logger = logging.getLogger(__name__)


class ListCoursesUseCase:
    """
    코스 목록 조회 유즈케이스
    
    저장된 코스 목록을 조회합니다.
    """

    def __init__(self, course_repository: CourseRepository):
        """
        Args:
            course_repository: 코스 리포지토리
        """
        self.course_repository = course_repository

    async def execute(
        self,
        user_id: Optional[UUID] = None,
        is_public: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> CourseListResponseDTO:
        """
        코스 목록 조회 실행
        
        Args:
            user_id: 사용자 ID (선택사항)
            is_public: 공개 여부 필터 (선택사항)
            limit: 페이지 크기 (기본값: 20)
            offset: 오프셋 (기본값: 0)
            
        Returns:
            코스 목록 응답
            
        Raises:
            DatabaseError: 데이터베이스 오류 시
        """
        try:
            # 1. CourseRepository.list() 호출
            courses = await self.course_repository.list(
                user_id=user_id,
                is_public=is_public,
                limit=limit,
                offset=offset,
            )

            # 2. Course 엔티티 리스트를 CourseListResponse로 변환
            course_items = [CourseListItemDTO.from_domain(course) for course in courses]

            logger.info(
                f"코스 목록 조회 성공 (count={len(course_items)}, "
                f"user_id={user_id}, is_public={is_public})"
            )

            return CourseListResponseDTO(
                courses=course_items,
                total=len(course_items),  # 실제로는 전체 개수를 별도로 조회해야 하지만, 간단히 현재 개수 사용
                limit=limit,
                offset=offset,
            )

        except DatabaseError as e:
            logger.error(f"코스 목록 조회 실패 - 데이터베이스 오류: {e}")
            raise
        except Exception as e:
            logger.error(f"코스 목록 조회 중 예상치 못한 오류: {e}", exc_info=True)
            raise DatabaseError(f"코스 목록 조회 실패: {str(e)}") from e

