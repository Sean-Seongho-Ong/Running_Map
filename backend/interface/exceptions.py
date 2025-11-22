"""
API Exception Handlers

FastAPI 예외 핸들러 및 커스텀 예외 매핑입니다.
"""

import logging
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError

from infrastructure.exceptions import (
    DatabaseError,
    DatabaseConnectionError,
    DatabaseTransactionError,
    CacheError,
    CacheConnectionError,
    ExternalServiceError,
    ExternalServiceTimeoutError,
    ExternalServiceRateLimitError,
)
from domain.services.loop_generator import LoopGenerationError

logger = logging.getLogger(__name__)


# APIErrorResponse는 실제로 사용되지 않으므로 제거
# FastAPI는 자동으로 JSONResponse를 생성하므로 별도 스키마 불필요


async def validation_exception_handler(
    request: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """
    Pydantic 검증 오류 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 검증 오류 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    errors = exc.errors() if hasattr(exc, "errors") else []
    error_details = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error.get("loc", []))
        error_details.append({
            "field": field,
            "message": error.get("msg"),
            "type": error.get("type"),
        })
    
    logger.warning(f"입력값 검증 실패: {error_details}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "입력값 검증 실패",
                "details": error_details,
            }
        },
    )


async def database_error_handler(request: Request, exc: DatabaseError) -> JSONResponse:
    """
    데이터베이스 오류 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 데이터베이스 오류 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    logger.error(f"데이터베이스 오류: {exc}", exc_info=True)
    
    if isinstance(exc, DatabaseConnectionError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        error_code = "DATABASE_CONNECTION_ERROR"
    elif isinstance(exc, DatabaseTransactionError):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = "DATABASE_TRANSACTION_ERROR"
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = "DATABASE_ERROR"
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": str(exc),
            }
        },
    )


async def cache_error_handler(request: Request, exc: CacheError) -> JSONResponse:
    """
    캐시 오류 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 캐시 오류 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    logger.error(f"캐시 오류: {exc}", exc_info=True)
    
    if isinstance(exc, CacheConnectionError):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        error_code = "CACHE_CONNECTION_ERROR"
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = "CACHE_ERROR"
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": "캐시 서비스 오류가 발생했습니다.",
            }
        },
    )


async def external_service_error_handler(
    request: Request, exc: ExternalServiceError
) -> JSONResponse:
    """
    외부 서비스 오류 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 외부 서비스 오류 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    logger.error(f"외부 서비스 오류: {exc}", exc_info=True)
    
    if isinstance(exc, ExternalServiceTimeoutError):
        status_code = status.HTTP_504_GATEWAY_TIMEOUT
        error_code = "EXTERNAL_SERVICE_TIMEOUT"
    elif isinstance(exc, ExternalServiceRateLimitError):
        status_code = status.HTTP_429_TOO_MANY_REQUESTS
        error_code = "EXTERNAL_SERVICE_RATE_LIMIT"
    else:
        status_code = status.HTTP_502_BAD_GATEWAY
        error_code = "EXTERNAL_SERVICE_ERROR"
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": str(exc),
            }
        },
    )


async def loop_generation_error_handler(
    request: Request, exc: LoopGenerationError
) -> JSONResponse:
    """
    루프 생성 오류 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 루프 생성 오류 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    logger.error(f"루프 생성 오류: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "COURSE_GENERATION_FAILED",
                "message": str(exc),
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    일반 예외 핸들러
    
    Args:
        request: FastAPI 요청 객체
        exc: 예외
        
    Returns:
        JSONResponse: 에러 응답
    """
    logger.error(f"예상치 못한 오류: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 오류가 발생했습니다.",
            }
        },
    )

