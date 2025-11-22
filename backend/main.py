"""
FastAPI Application Entry Point

FastAPI 애플리케이션을 초기화하고 설정합니다.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

from config import settings
from infrastructure.exceptions import (
    DatabaseError,
    CacheError,
    ExternalServiceError,
)
from domain.services.loop_generator import LoopGenerationError
from interface.exceptions import (
    validation_exception_handler,
    database_error_handler,
    cache_error_handler,
    external_service_error_handler,
    loop_generation_error_handler,
    generic_exception_handler,
)

# 로거 설정
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 생명주기 관리"""
    # Startup
    logger.info(
        "application_started",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
    )
    yield
    # Shutdown
    logger.info("application_shutdown")


# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="러닝 코스 자동 생성 및 추적 모바일 애플리케이션 API",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 예외 핸들러 등록
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(CacheError, cache_error_handler)
app.add_exception_handler(ExternalServiceError, external_service_error_handler)
app.add_exception_handler(LoopGenerationError, loop_generation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


# API 라우터 등록
from interface.api.v1.routes import courses, running

app.include_router(
    courses.router,
    prefix=settings.API_V1_PREFIX,
    tags=["courses"],
)
app.include_router(
    running.router,
    prefix=settings.API_V1_PREFIX,
    tags=["running"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )

