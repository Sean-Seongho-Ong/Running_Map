"""
Course DTO Tests

Course 관련 DTO의 단위 테스트입니다.
"""

import pytest
from uuid import uuid4

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
from domain.entities.course import Course, CourseMetadata
from domain.entities.route import Route
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


class TestCoordinateDTO:
    """CoordinateDTO 테스트"""

    def test_create_valid_coordinate(self):
        """유효한 좌표 생성 테스트"""
        coord = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        assert coord.latitude == 37.5665
        assert coord.longitude == 126.9780

    def test_create_invalid_latitude(self):
        """잘못된 위도 검증 테스트"""
        with pytest.raises(ValueError):
            CoordinateDTO(latitude=91.0, longitude=126.9780)

    def test_create_invalid_longitude(self):
        """잘못된 경도 검증 테스트"""
        with pytest.raises(ValueError):
            CoordinateDTO(latitude=37.5665, longitude=181.0)

    def test_to_domain(self):
        """도메인 Coordinate로 변환 테스트"""
        coord_dto = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        coord = coord_dto.to_domain()
        assert isinstance(coord, Coordinate)
        assert coord.latitude == 37.5665
        assert coord.longitude == 126.9780

    def test_from_domain(self):
        """도메인 Coordinate에서 생성 테스트"""
        coord = Coordinate(latitude=37.5665, longitude=126.9780)
        coord_dto = CoordinateDTO.from_domain(coord)
        assert coord_dto.latitude == 37.5665
        assert coord_dto.longitude == 126.9780


class TestCourseGenerationParametersDTO:
    """CourseGenerationParametersDTO 테스트"""

    def test_create_with_defaults(self):
        """기본값으로 생성 테스트"""
        params = CourseGenerationParametersDTO()
        assert params.step_init == 1.0
        assert params.step_min == 0.4
        assert params.step_max == 2.0
        assert params.tolerance_ratio == 0.1
        assert params.shrink_factor == 0.8
        assert params.grow_factor == 1.2
        assert params.max_iter == 5
        assert params.use_SP_fallback is True

    def test_create_with_custom_values(self):
        """사용자 정의 값으로 생성 테스트"""
        params = CourseGenerationParametersDTO(
            step_init=1.5,
            step_min=0.5,
            step_max=3.0,
            tolerance_ratio=0.15,
            max_iter=10,
        )
        assert params.step_init == 1.5
        assert params.max_iter == 10


class TestCourseGenerationRequestDTO:
    """CourseGenerationRequestDTO 테스트"""

    def test_create_valid_request(self):
        """유효한 요청 생성 테스트"""
        start_point = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        request = CourseGenerationRequestDTO(
            start_point=start_point, target_distance=10.0
        )
        assert request.start_point.latitude == 37.5665
        assert request.target_distance == 10.0

    def test_create_with_parameters(self):
        """파라미터 포함 요청 생성 테스트"""
        start_point = CoordinateDTO(latitude=37.5665, longitude=126.9780)
        params = CourseGenerationParametersDTO(step_init=1.5)
        request = CourseGenerationRequestDTO(
            start_point=start_point, target_distance=10.0, parameters=params
        )
        assert request.parameters is not None
        assert request.parameters.step_init == 1.5


class TestCourseMetadataDTO:
    """CourseMetadataDTO 테스트"""

    def test_to_domain(self):
        """도메인 CourseMetadata로 변환 테스트"""
        metadata_dto = CourseMetadataDTO(
            estimated_time=30,
            elevation_gain=150.0,
            difficulty="medium",
        )
        metadata = metadata_dto.to_domain()
        assert isinstance(metadata, CourseMetadata)
        assert metadata.estimated_time == 30
        assert metadata.elevation_gain == 150.0
        assert metadata.difficulty == "medium"

    def test_from_domain(self):
        """도메인 CourseMetadata에서 생성 테스트"""
        metadata = CourseMetadata(
            estimated_time=30,
            elevation_gain=150.0,
            difficulty="medium",
        )
        metadata_dto = CourseMetadataDTO.from_domain(metadata)
        assert metadata_dto.estimated_time == 30
        assert metadata_dto.elevation_gain == 150.0
        assert metadata_dto.difficulty == "medium"


class TestCourseGenerationResultDTO:
    """CourseGenerationResultDTO 테스트"""

    def test_from_route(self):
        """도메인 Route에서 생성 테스트"""
        polyline = [
            Coordinate(latitude=37.5665, longitude=126.9780),
            Coordinate(latitude=37.5670, longitude=126.9785),
        ]
        route = Route(
            polyline=polyline,
            distance=Distance.from_kilometers(5.0),
            algorithm="STEP_ADAPTIVE",
            iterations=3,
            step_used=1.0,
            relative_error=0.05,
        )
        result = CourseGenerationResultDTO.from_route(route)
        assert result.distance == 5.0
        assert result.algorithm == "STEP_ADAPTIVE"
        assert result.iterations == 3
        assert result.relative_error == 0.05


class TestCourseSaveRequestDTO:
    """CourseSaveRequestDTO 테스트"""

    def test_to_domain(self):
        """도메인 Course로 변환 테스트"""
        polyline = [
            CoordinateDTO(latitude=37.5665, longitude=126.9780),
            CoordinateDTO(latitude=37.5670, longitude=126.9785),
        ]
        request = CourseSaveRequestDTO(
            name="테스트 코스",
            polyline=polyline,
            distance=5.0,
            is_public=True,
        )
        course = request.to_domain()
        assert isinstance(course, Course)
        assert course.name == "테스트 코스"
        assert course.distance.kilometers == 5.0
        assert course.is_public is True


class TestCourseSaveResponseDTO:
    """CourseSaveResponseDTO 테스트"""

    def test_from_domain(self):
        """도메인 Course에서 생성 테스트"""
        polyline = [
            Coordinate(latitude=37.5665, longitude=126.9780),
            Coordinate(latitude=37.5670, longitude=126.9785),
        ]
        course = Course(
            name="테스트 코스",
            polyline=polyline,
            distance=Distance.from_kilometers(5.0),
        )
        response = CourseSaveResponseDTO.from_domain(course)
        assert response.id == course.id
        assert response.name == "테스트 코스"


class TestCourseListResponseDTO:
    """CourseListResponseDTO 테스트"""

    def test_create_response(self):
        """응답 생성 테스트"""
        polyline = [
            Coordinate(latitude=37.5665, longitude=126.9780),
            Coordinate(latitude=37.5670, longitude=126.9785),
        ]
        course = Course(
            name="테스트 코스",
            polyline=polyline,
            distance=Distance.from_kilometers(5.0),
        )
        item = CourseListItemDTO.from_domain(course)
        response = CourseListResponseDTO(
            courses=[item], total=1, limit=20, offset=0
        )
        assert len(response.courses) == 1
        assert response.total == 1
        assert response.limit == 20

