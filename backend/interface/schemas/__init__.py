"""
API Schemas

FastAPI에서 사용하는 Pydantic 스키마입니다.
Application DTO를 재사용하거나 API 스키마로 변환합니다.
"""

from application.dto.course_dto import (
    CoordinateDTO,
    CourseDeleteResponseDTO,
    CourseDetailResponseDTO,
    CourseGenerationParametersDTO,
    CourseGenerationRequestDTO,
    CourseGenerationResponseDTO,
    CourseGenerationResultDTO,
    CourseListResponseDTO,
    CourseListItemDTO,
    CourseMetadataDTO,
    CourseSaveRequestDTO,
    CourseSaveResponseDTO,
)
from application.dto.running_dto import (
    LocationDTO,
    LocationUpdateRequestDTO,
    LocationUpdateResponseDTO,
    RunningSessionFinishRequestDTO,
    RunningSessionFinishResponseDTO,
    RunningSessionStartRequestDTO,
    RunningSessionStartResponseDTO,
    RunningSessionUpdateRequestDTO,
    RunningSessionUpdateResponseDTO,
    RunningStatsDTO,
)

# API 스키마는 Application DTO를 그대로 재사용
__all__ = [
    # Course schemas
    "CoordinateDTO",
    "CourseGenerationParametersDTO",
    "CourseGenerationRequestDTO",
    "CourseGenerationResponseDTO",
    "CourseGenerationResultDTO",
    "CourseMetadataDTO",
    "CourseSaveRequestDTO",
    "CourseSaveResponseDTO",
    "CourseListResponseDTO",
    "CourseListItemDTO",
    "CourseDetailResponseDTO",
    "CourseDeleteResponseDTO",
    # Running schemas
    "LocationDTO",
    "RunningSessionStartRequestDTO",
    "RunningSessionStartResponseDTO",
    "RunningSessionUpdateRequestDTO",
    "RunningSessionUpdateResponseDTO",
    "LocationUpdateRequestDTO",
    "LocationUpdateResponseDTO",
    "RunningSessionFinishRequestDTO",
    "RunningSessionFinishResponseDTO",
    "RunningStatsDTO",
]
