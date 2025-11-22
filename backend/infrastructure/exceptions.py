"""
Infrastructure Exceptions

인프라 계층에서 사용하는 커스텀 예외입니다.
"""


class InfrastructureError(Exception):
    """인프라 계층 기본 예외"""
    pass


class DatabaseError(InfrastructureError):
    """데이터베이스 관련 오류"""
    pass


class DatabaseConnectionError(DatabaseError):
    """데이터베이스 연결 오류"""
    pass


class DatabaseTransactionError(DatabaseError):
    """데이터베이스 트랜잭션 오류"""
    pass


class CacheError(InfrastructureError):
    """캐시 관련 오류"""
    pass


class CacheConnectionError(CacheError):
    """캐시 연결 오류"""
    pass


class ExternalServiceError(InfrastructureError):
    """외부 서비스 관련 오류"""
    pass


class ExternalServiceTimeoutError(ExternalServiceError):
    """외부 서비스 타임아웃 오류"""
    pass


class ExternalServiceRateLimitError(ExternalServiceError):
    """외부 서비스 Rate Limit 오류"""
    pass

