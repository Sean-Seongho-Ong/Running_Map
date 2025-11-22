"""
Running Session Repository Interface

러닝 세션 리포지토리 인터페이스입니다.
"""

from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities.running_session import RunningSession


class RunningSessionRepository(ABC):
    """
    러닝 세션 리포지토리 인터페이스
    
    러닝 세션의 영속성을 관리합니다.
    """

    @abstractmethod
    async def create(self, session: RunningSession) -> RunningSession:
        """
        러닝 세션을 생성합니다.
        
        Args:
            session: 생성할 세션
            
        Returns:
            생성된 세션
        """
        pass

    @abstractmethod
    async def get_by_id(self, session_id: UUID) -> Optional[RunningSession]:
        """
        ID로 러닝 세션을 조회합니다.
        
        Args:
            session_id: 세션 ID
            
        Returns:
            러닝 세션 (없으면 None)
        """
        pass

    @abstractmethod
    async def update(self, session: RunningSession) -> RunningSession:
        """
        러닝 세션을 업데이트합니다.
        
        Args:
            session: 업데이트할 세션
            
        Returns:
            업데이트된 세션
        """
        pass

