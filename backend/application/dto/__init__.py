"""
Data Transfer Objects (DTOs)

API와 도메인 계층 간 데이터 전송을 위한 객체들입니다.
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

__all__ = [
    # Course DTOs
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
    # Running DTOs
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
