"""
Course API Routes

코스 관련 API 엔드포인트입니다.
"""

import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse

from interface.schemas import (
    CourseGenerationRequestDTO,
    CourseGenerationResponseDTO,
    CourseSaveRequestDTO,
    CourseSaveResponseDTO,
    CourseListResponseDTO,
    CourseDetailResponseDTO,
    CourseDeleteResponseDTO,
)
from interface.dependencies import (
    GenerateCourseUseCaseDep,
    SaveCourseUseCaseDep,
    ListCoursesUseCaseDep,
    GetCourseUseCaseDep,
    DeleteCourseUseCaseDep,
)
from infrastructure.exceptions import DatabaseError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post(
    "/generate",
    response_model=CourseGenerationResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="코스 생성",
    description="""
    사용자 위치와 목표 거리를 기반으로 Distance-Constrained Loop Generation Algorithm을 사용하여
    러닝 코스를 자동 생성합니다.
    
    알고리즘:
    - Step 기반 원둘레 분할 + 양방향 Adaptive Step 피드백
    - S-P 기반 Fallback
    - 최종 Fallback (Out & Back)
    """,
)
async def generate_course(
    request: CourseGenerationRequestDTO,
    use_case: GenerateCourseUseCaseDep,
) -> CourseGenerationResponseDTO:
    """
    코스 생성 엔드포인트
    
    Args:
        request: 코스 생성 요청
        use_case: GenerateCourseUseCase
        
    Returns:
        코스 생성 응답
    """
    try:
        response = await use_case.execute(request)
        return response
    except Exception as e:
        logger.error(f"코스 생성 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="코스 생성 중 오류가 발생했습니다.",
        )


@router.post(
    "",
    response_model=CourseSaveResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="코스 저장",
    description="생성된 코스를 서버에 저장합니다.",
)
async def save_course(
    request: CourseSaveRequestDTO,
    use_case: SaveCourseUseCaseDep,
) -> CourseSaveResponseDTO:
    """
    코스 저장 엔드포인트
    
    Args:
        request: 코스 저장 요청
        use_case: SaveCourseUseCase
        
    Returns:
        코스 저장 응답
    """
    try:
        response = await use_case.execute(request)
        return response
    except DatabaseError as e:
        logger.error(f"코스 저장 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"코스 저장 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="코스 저장 중 오류가 발생했습니다.",
        )


@router.get(
    "",
    response_model=CourseListResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="코스 목록 조회",
    description="저장된 코스 목록을 조회합니다.",
)
async def list_courses(
    user_id: Optional[UUID] = Query(None, description="사용자 ID (필터)"),
    is_public: Optional[bool] = Query(None, description="공개 여부 (필터)"),
    limit: int = Query(20, ge=1, le=100, description="페이지 크기"),
    offset: int = Query(0, ge=0, description="오프셋"),
    use_case: ListCoursesUseCaseDep = None,
) -> CourseListResponseDTO:
    """
    코스 목록 조회 엔드포인트
    
    Args:
        user_id: 사용자 ID (선택사항)
        is_public: 공개 여부 (선택사항)
        limit: 페이지 크기
        offset: 오프셋
        use_case: ListCoursesUseCase
        
    Returns:
        코스 목록 응답
    """
    try:
        response = await use_case.execute(
            user_id=user_id,
            is_public=is_public,
            limit=limit,
            offset=offset,
        )
        return response
    except DatabaseError as e:
        logger.error(f"코스 목록 조회 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"코스 목록 조회 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="코스 목록 조회 중 오류가 발생했습니다.",
        )


@router.get(
    "/{course_id}",
    response_model=CourseDetailResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="코스 상세 조회",
    description="저장된 코스의 상세 정보를 조회합니다.",
)
async def get_course(
    course_id: UUID,
    use_case: GetCourseUseCaseDep,
) -> CourseDetailResponseDTO:
    """
    코스 상세 조회 엔드포인트
    
    Args:
        course_id: 코스 ID
        use_case: GetCourseUseCase
        
    Returns:
        코스 상세 응답
    """
    try:
        response = await use_case.execute(course_id)
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"코스를 찾을 수 없습니다 (id={course_id})",
            )
        return response
    except HTTPException:
        raise
    except DatabaseError as e:
        logger.error(f"코스 상세 조회 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"코스 상세 조회 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="코스 상세 조회 중 오류가 발생했습니다.",
        )


@router.delete(
    "/{course_id}",
    response_model=CourseDeleteResponseDTO,
    status_code=status.HTTP_200_OK,
    summary="코스 삭제",
    description="저장된 코스를 삭제합니다.",
)
async def delete_course(
    course_id: UUID,
    use_case: DeleteCourseUseCaseDep,
) -> CourseDeleteResponseDTO:
    """
    코스 삭제 엔드포인트
    
    Args:
        course_id: 코스 ID
        use_case: DeleteCourseUseCase
        
    Returns:
        코스 삭제 응답
    """
    try:
        response = await use_case.execute(course_id)
        return response
    except DatabaseError as e:
        logger.error(f"코스 삭제 실패: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"코스 삭제 중 오류: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="코스 삭제 중 오류가 발생했습니다.",
        )

