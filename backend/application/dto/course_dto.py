"""
Course DTOs

코스 관련 데이터 전송 객체입니다.
OpenAPI 명세서를 기반으로 정의됩니다.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from domain.entities.course import Course, CourseMetadata
from domain.entities.route import Route
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class CoordinateDTO(BaseModel):
    """좌표 DTO"""

    latitude: float = Field(..., ge=-90, le=90, description="위도 (WGS84)")
    longitude: float = Field(..., ge=-180, le=180, description="경도 (WGS84)")

    def to_domain(self) -> Coordinate:
        """도메인 Coordinate로 변환"""
        return Coordinate(latitude=self.latitude, longitude=self.longitude)

    @classmethod
    def from_domain(cls, coordinate: Coordinate) -> "CoordinateDTO":
        """도메인 Coordinate에서 생성"""
        return cls(latitude=coordinate.latitude, longitude=coordinate.longitude)


class CourseGenerationParametersDTO(BaseModel):
    """코스 생성 알고리즘 파라미터 DTO"""

    step_init: float = Field(default=1.0, ge=0.1, le=5.0, description="초기 스텝 길이 (km)")
    step_min: float = Field(default=0.4, ge=0.1, le=2.0, description="최소 스텝 길이 (km)")
    step_max: float = Field(default=2.0, ge=0.5, le=5.0, description="최대 스텝 길이 (km)")
    tolerance_ratio: float = Field(default=0.1, ge=0.0, le=1.0, description="허용 오차 비율")
    shrink_factor: float = Field(default=0.8, ge=0.1, le=1.0, description="Step 축소 계수")
    grow_factor: float = Field(default=1.2, ge=1.0, le=3.0, description="Step 확대 계수")
    max_iter: int = Field(default=5, ge=1, le=20, description="최대 반복 횟수")
    use_SP_fallback: bool = Field(default=True, description="S-P 기반 Fallback 사용 여부")


class CourseGenerationRequestDTO(BaseModel):
    """코스 생성 요청 DTO"""

    start_point: CoordinateDTO = Field(..., description="시작점 좌표")
    target_distance: float = Field(..., ge=0.5, le=50.0, description="목표 거리 (km)")
    parameters: Optional[CourseGenerationParametersDTO] = Field(
        default=None, description="알고리즘 파라미터"
    )


class CourseMetadataDTO(BaseModel):
    """코스 메타데이터 DTO"""

    estimated_time: Optional[int] = Field(default=None, ge=0, description="예상 소요 시간 (분)")
    elevation_gain: Optional[float] = Field(default=None, ge=0, description="누적 상승 고도 (m)")
    elevation_loss: Optional[float] = Field(default=None, ge=0, description="누적 하강 고도 (m)")
    quality_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="코스 품질 점수 (0.0 ~ 1.0)"
    )
    self_intersections: Optional[int] = Field(
        default=None, ge=0, description="자가 교차 횟수"
    )
    tags: list[str] = Field(default_factory=list, description="코스 태그")
    difficulty: Optional[str] = Field(
        default=None, description="난이도", pattern="^(easy|medium|hard)$"
    )

    def to_domain(self) -> CourseMetadata:
        """도메인 CourseMetadata로 변환"""
        return CourseMetadata(
            estimated_time=self.estimated_time,
            elevation_gain=self.elevation_gain,
            elevation_loss=self.elevation_loss,
            quality_score=self.quality_score,
            self_intersections=self.self_intersections,
            tags=self.tags,
            difficulty=self.difficulty,
        )

    @classmethod
    def from_domain(cls, metadata: CourseMetadata) -> "CourseMetadataDTO":
        """도메인 CourseMetadata에서 생성"""
        return cls(
            estimated_time=metadata.estimated_time,
            elevation_gain=metadata.elevation_gain,
            elevation_loss=metadata.elevation_loss,
            quality_score=metadata.quality_score,
            self_intersections=metadata.self_intersections,
            tags=metadata.tags,
            difficulty=metadata.difficulty,
        )


class CourseGenerationResultDTO(BaseModel):
    """코스 생성 결과 DTO"""

    id: UUID = Field(..., description="임시 코스 ID (저장 전)")
    polyline: list[CoordinateDTO] = Field(..., min_length=2, description="폴리라인 좌표 배열")
    distance: float = Field(..., ge=0, description="실제 코스 거리 (km)")
    relative_error: float = Field(..., description="상대 오차 (|L - D| / D)")
    algorithm: str = Field(
        ..., description="사용된 알고리즘", pattern="^(STEP_ADAPTIVE|SP_BASED|FALLBACK)$"
    )
    iterations: int = Field(default=0, ge=0, description="반복 횟수")
    step_used: Optional[float] = Field(default=None, description="사용된 step 값 (km)")
    metadata: Optional[CourseMetadataDTO] = Field(default=None, description="코스 메타데이터")

    @classmethod
    def from_route(cls, route: Route, metadata: Optional[CourseMetadata] = None) -> "CourseGenerationResultDTO":
        """도메인 Route에서 생성"""
        return cls(
            id=route.id,
            polyline=[CoordinateDTO.from_domain(coord) for coord in route.polyline],
            distance=route.distance.kilometers,
            relative_error=route.relative_error,
            algorithm=route.algorithm,
            iterations=route.iterations,
            step_used=route.step_used,
            metadata=CourseMetadataDTO.from_domain(metadata) if metadata else None,
        )


class CourseGenerationResponseDTO(BaseModel):
    """코스 생성 응답 DTO"""

    status: str = Field(..., description="생성 상태", pattern="^(OK|BEST_EFFORT|FAIL)$")
    course: Optional[CourseGenerationResultDTO] = Field(default=None, description="생성된 코스")
    error: Optional[dict] = Field(default=None, description="에러 정보")


class CourseSaveRequestDTO(BaseModel):
    """코스 저장 요청 DTO"""

    name: str = Field(..., min_length=1, max_length=255, description="코스 이름")
    polyline: list[CoordinateDTO] = Field(..., min_length=2, description="폴리라인 좌표 배열")
    distance: float = Field(..., ge=0, description="코스 거리 (km)")
    metadata: Optional[CourseMetadataDTO] = Field(default=None, description="코스 메타데이터")
    is_public: bool = Field(default=False, description="공개 여부")

    def to_domain(self) -> Course:
        """도메인 Course로 변환"""
        polyline = [coord.to_domain() for coord in self.polyline]
        metadata = self.metadata.to_domain() if self.metadata else CourseMetadata()
        
        return Course(
            name=self.name,
            polyline=polyline,
            distance=Distance.from_kilometers(self.distance),
            metadata=metadata,
            is_public=self.is_public,
        )


class CourseSaveResponseDTO(BaseModel):
    """코스 저장 응답 DTO"""

    id: UUID = Field(..., description="코스 ID")
    name: str = Field(..., description="코스 이름")
    created_at: datetime = Field(..., description="생성일시")

    @classmethod
    def from_domain(cls, course: Course) -> "CourseSaveResponseDTO":
        """도메인 Course에서 생성"""
        return cls(
            id=course.id,
            name=course.name,
            created_at=course.created_at,
        )


class CourseListItemDTO(BaseModel):
    """코스 목록 항목 DTO"""

    id: UUID = Field(..., description="코스 ID")
    name: str = Field(..., description="코스 이름")
    distance: float = Field(..., description="코스 거리 (km)")
    is_public: bool = Field(..., description="공개 여부")
    created_at: datetime = Field(..., description="생성일시")

    @classmethod
    def from_domain(cls, course: Course) -> "CourseListItemDTO":
        """도메인 Course에서 생성"""
        return cls(
            id=course.id,
            name=course.name,
            distance=course.distance.kilometers,
            is_public=course.is_public,
            created_at=course.created_at,
        )


class CourseListResponseDTO(BaseModel):
    """코스 목록 응답 DTO"""

    courses: list[CourseListItemDTO] = Field(..., description="코스 목록")
    total: int = Field(..., ge=0, description="전체 코스 수")
    limit: int = Field(..., ge=1, description="페이지 크기")
    offset: int = Field(..., ge=0, description="오프셋")


class CourseDetailResponseDTO(BaseModel):
    """코스 상세 응답 DTO"""

    id: UUID = Field(..., description="코스 ID")
    name: str = Field(..., description="코스 이름")
    polyline: list[CoordinateDTO] = Field(..., min_length=2, description="폴리라인 좌표 배열")
    distance: float = Field(..., ge=0, description="코스 거리 (km)")
    metadata: Optional[CourseMetadataDTO] = Field(default=None, description="코스 메타데이터")
    is_public: bool = Field(..., description="공개 여부")
    user_id: Optional[UUID] = Field(default=None, description="사용자 ID")
    created_at: datetime = Field(..., description="생성일시")
    updated_at: Optional[datetime] = Field(default=None, description="수정일시")

    @classmethod
    def from_domain(cls, course: Course) -> "CourseDetailResponseDTO":
        """도메인 Course에서 생성"""
        return cls(
            id=course.id,
            name=course.name,
            polyline=[CoordinateDTO.from_domain(coord) for coord in course.polyline],
            distance=course.distance.kilometers,
            metadata=CourseMetadataDTO.from_domain(course.metadata) if course.metadata else None,
            is_public=course.is_public,
            user_id=course.user_id,
            created_at=course.created_at,
            updated_at=course.updated_at,
        )


class CourseDeleteResponseDTO(BaseModel):
    """코스 삭제 응답 DTO"""

    success: bool = Field(..., description="삭제 성공 여부")
    course_id: UUID = Field(..., description="삭제된 코스 ID")

