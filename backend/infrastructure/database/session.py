"""
Database Session Management

SQLAlchemy 비동기 세션을 관리합니다.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from infrastructure.config.settings import settings

# 비동기 엔진 생성
engine = create_async_engine(
    settings.database_url,
    echo=settings.DB_ECHO,
    future=True,
)

# 비동기 세션 팩토리
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    데이터베이스 세션 의존성 주입 함수
    
    FastAPI의 Depends()와 함께 사용합니다.
    
    Yields:
        AsyncSession: 데이터베이스 세션
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """
    데이터베이스 초기화
    
    테이블을 생성합니다. (개발 환경에서만 사용)
    """
    from infrastructure.database.models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    데이터베이스 연결 종료
    """
    await engine.dispose()

