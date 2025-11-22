"""
Course Repository Interface

코스 리포지토리 인터페이스입니다.
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.course import Course


class CourseRepository(ABC):
    """
    코스 리포지토리 인터페이스
    
    코스의 영속성을 관리합니다.
    """

    @abstractmethod
    async def create(self, course: Course) -> Course:
        """
        코스를 생성합니다.
        
        Args:
            course: 생성할 코스
            
        Returns:
            생성된 코스
        """
        pass

    @abstractmethod
    async def get_by_id(self, course_id: UUID) -> Optional[Course]:
        """
        ID로 코스를 조회합니다.
        
        Args:
            course_id: 코스 ID
            
        Returns:
            코스 (없으면 None)
        """
        pass

    @abstractmethod
    async def list(
        self,
        user_id: Optional[UUID] = None,
        is_public: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Course]:
        """
        코스 목록을 조회합니다.
        
        Args:
            user_id: 사용자 ID (선택사항)
            is_public: 공개 여부 (선택사항)
            limit: 페이지당 항목 수
            offset: 페이지 오프셋
            
        Returns:
            코스 목록
        """
        pass

    @abstractmethod
    async def update(self, course: Course) -> Course:
        """
        코스를 업데이트합니다.
        
        Args:
            course: 업데이트할 코스
            
        Returns:
            업데이트된 코스
        """
        pass

    @abstractmethod
    async def delete(self, course_id: UUID) -> bool:
        """
        코스를 삭제합니다.
        
        Args:
            course_id: 코스 ID
            
        Returns:
            삭제 성공 여부
        """
        pass

