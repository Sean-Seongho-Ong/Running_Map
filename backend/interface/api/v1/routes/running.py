"""
Running API Routes

러닝 세션 관련 API 엔드포인트입니다.
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from interface.schemas import (
    RunningSessionStartRequestDTO,
    RunningSessionStartResponseDTO,
    RunningSessionUpdateRequestDTO,
    RunningSessionUpdateResponseDTO,
    LocationUpdateRequestDTO,
    LocationUpdateResponseDTO,
    RunningSessionFinishRequestDTO,
    RunningSessionFinishResponseDTO,
)
from interface.dependencies import (
    StartRunningUseCaseDep,
    UpdateRunningUseCaseDep,
    UpdateLocationUseCaseDep,
    FinishRunningUseCaseDep,
)
from infrastructure.exceptions import DatabaseError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/running", tags=["running"])


@router.post(
    "/start",
    response_model=RunningSessionStartResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="러닝 세션 시작",
    description="새로운 러닝 세션을 시작합니다. 선택적으로 기존 코스를 사용할 수 있습니다.",
)
async def start_running(
    request: RunningSessionStartRequestDTO,
    use_case: StartRunningUseCaseDep,
) -> RunningSessionStartResponseDTO:
    """
    러닝 세션 시작 엔드포인트
    
    Args:
        request: 러닝 시작 요청
        use_case: StartRunningUseCase
        
    Returns:
        러닝 시작 응답
    """
    try:
        response = await use_case.execute(request)
        return response
    except ValueError as e:
        logger.error(f"러닝 세션 시작 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except DatabaseError as e:
        logger.error(f"러닝 세션 시작 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"러닝 세션 시작 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="러닝 세션 시작 중 오류가 발생했습니다.",
        )


@router.put(
    "/{session_id}",
    response_model=RunningSessionUpdateResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="러닝 세션 업데이트",
    description="러닝 세션의 현재 상태를 업데이트합니다.",
)
async def update_running(
    session_id: UUID,
    request: RunningSessionUpdateRequestDTO,
    use_case: UpdateRunningUseCaseDep,
) -> RunningSessionUpdateResponseDTO:
    """
    러닝 세션 업데이트 엔드포인트
    
    Args:
        session_id: 러닝 세션 ID
        request: 러닝 업데이트 요청
        use_case: UpdateRunningUseCase
        
    Returns:
        러닝 업데이트 응답
    """
    try:
        response = await use_case.execute(session_id, request)
        return response
    except ValueError as e:
        logger.error(f"러닝 세션 업데이트 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DatabaseError as e:
        logger.error(f"러닝 세션 업데이트 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"러닝 세션 업데이트 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="러닝 세션 업데이트 중 오류가 발생했습니다.",
        )


@router.post(
    "/{session_id}/location",
    response_model=LocationUpdateResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="위치 업데이트",
    description="러닝 중 현재 위치를 업데이트하고 통계를 계산합니다.",
)
async def update_location(
    session_id: UUID,
    request: LocationUpdateRequestDTO,
    use_case: UpdateLocationUseCaseDep,
) -> LocationUpdateResponseDTO:
    """
    위치 업데이트 엔드포인트
    
    Args:
        session_id: 러닝 세션 ID
        request: 위치 업데이트 요청
        use_case: UpdateLocationUseCase
        
    Returns:
        위치 업데이트 응답
    """
    try:
        response = await use_case.execute(session_id, request)
        return response
    except ValueError as e:
        logger.error(f"위치 업데이트 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DatabaseError as e:
        logger.error(f"위치 업데이트 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"위치 업데이트 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="위치 업데이트 중 오류가 발생했습니다.",
        )


@router.post(
    "/{session_id}/finish",
    response_model=RunningSessionFinishResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="러닝 세션 종료",
    description="러닝 세션을 종료하고 최종 통계를 반환합니다.",
)
async def finish_running(
    session_id: UUID,
    request: RunningSessionFinishRequestDTO,
    use_case: FinishRunningUseCaseDep,
) -> RunningSessionFinishResponseDTO:
    """
    러닝 세션 종료 엔드포인트
    
    Args:
        session_id: 러닝 세션 ID
        request: 러닝 종료 요청
        use_case: FinishRunningUseCase
        
    Returns:
        러닝 종료 응답
    """
    try:
        response = await use_case.execute(session_id, request)
        return response
    except ValueError as e:
        logger.error(f"러닝 세션 종료 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DatabaseError as e:
        logger.error(f"러닝 세션 종료 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"러닝 세션 종료 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="러닝 세션 종료 중 오류가 발생했습니다.",
        )

