"""
Course API Tests

코스 관련 API 엔드포인트 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from starlette.testclient import TestClient

from main import app
import interface.dependencies
from application.dto.course_dto import (
    CourseGenerationRequestDTO,
    CourseGenerationResponseDTO,
    CourseGenerationResultDTO,
    CourseSaveRequestDTO,
    CourseSaveResponseDTO,
    CourseListResponseDTO,
    CourseDetailResponseDTO,
    CourseDeleteResponseDTO,
    CoordinateDTO,
)
from domain.entities.course import Course
from domain.entities.route import Route
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance


@pytest.fixture
def client():
    """FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_dependency_overrides():
    """각 테스트 후 의존성 오버라이드 초기화"""
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def mock_generate_course_use_case():
    """Mock GenerateCourseUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_save_course_use_case():
    """Mock SaveCourseUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_list_courses_use_case():
    """Mock ListCoursesUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_get_course_use_case():
    """Mock GetCourseUseCase"""
    use_case = AsyncMock()
    return use_case


@pytest.fixture
def mock_delete_course_use_case():
    """Mock DeleteCourseUseCase"""
    use_case = AsyncMock()
    return use_case


class TestGenerateCourseAPI:
    """코스 생성 API 테스트"""

    def test_generate_course_success(self, client, mock_generate_course_use_case):
        """코스 생성 성공 테스트"""
        # Mock 응답 설정
        response_dto = CourseGenerationResponseDTO(
            status="OK",
            course=CourseGenerationResultDTO(
                id=uuid4(),
                polyline=[
                    CoordinateDTO(latitude=37.5665, longitude=126.9780),
                    CoordinateDTO(latitude=37.5670, longitude=126.9785),
                ],
                distance=10.0,
                relative_error=0.05,
                algorithm="STEP_ADAPTIVE",
                iterations=3,
                step_used=1.0,
            ),
        )
        mock_generate_course_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_generate_course_use_case
        ] = lambda: mock_generate_course_use_case
        
        request_data = {
            "start_point": {"latitude": 37.5665, "longitude": 126.9780},
            "target_distance": 10.0,
        }
        response = client.post("/api/v1/courses/generate", json=request_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert data["course"] is not None
        assert data["course"]["distance"] == 10.0

    def test_generate_course_validation_error(self, client):
        """코스 생성 검증 오류 테스트"""
        request_data = {
            "start_point": {"latitude": 91.0, "longitude": 126.9780},  # 잘못된 위도
            "target_distance": 10.0,
        }
        response = client.post("/api/v1/courses/generate", json=request_data)

        assert response.status_code == 400
        data = response.json()
        assert "error" in data


class TestSaveCourseAPI:
    """코스 저장 API 테스트"""

    def test_save_course_success(self, client, mock_save_course_use_case):
        """코스 저장 성공 테스트"""
        course_id = uuid4()
        response_dto = CourseSaveResponseDTO(
            id=course_id,
            name="테스트 코스",
            created_at="2024-01-01T00:00:00Z",
        )
        mock_save_course_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_save_course_use_case
        ] = lambda: mock_save_course_use_case
        
        request_data = {
            "name": "테스트 코스",
            "polyline": [
                {"latitude": 37.5665, "longitude": 126.9780},
                {"latitude": 37.5670, "longitude": 126.9785},
            ],
            "distance": 5.0,
        }
        response = client.post("/api/v1/courses", json=request_data)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "테스트 코스"


class TestListCoursesAPI:
    """코스 목록 API 테스트"""

    def test_list_courses_success(self, client, mock_list_courses_use_case):
        """코스 목록 조회 성공 테스트"""
        response_dto = CourseListResponseDTO(
            courses=[],
            total=0,
            limit=20,
            offset=0,
        )
        mock_list_courses_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_list_courses_use_case
        ] = lambda: mock_list_courses_use_case
        
        response = client.get("/api/v1/courses")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["limit"] == 20


class TestGetCourseAPI:
    """코스 상세 API 테스트"""

    def test_get_course_success(self, client, mock_get_course_use_case):
        """코스 상세 조회 성공 테스트"""
        course_id = uuid4()
        response_dto = CourseDetailResponseDTO(
            id=course_id,
            name="테스트 코스",
            distance=5.0,
            polyline=[
                CoordinateDTO(latitude=37.5665, longitude=126.9780),
                CoordinateDTO(latitude=37.5670, longitude=126.9785),
            ],
            is_public=False,
            created_at="2024-01-01T00:00:00Z",
        )
        mock_get_course_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_get_course_use_case
        ] = lambda: mock_get_course_use_case
        
        response = client.get(f"/api/v1/courses/{course_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "테스트 코스"

    def test_get_course_not_found(self, client, mock_get_course_use_case):
        """코스 없음 테스트"""
        course_id = uuid4()
        mock_get_course_use_case.execute.return_value = None

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_get_course_use_case
        ] = lambda: mock_get_course_use_case
        
        response = client.get(f"/api/v1/courses/{course_id}")

        assert response.status_code == 404


class TestDeleteCourseAPI:
    """코스 삭제 API 테스트"""

    def test_delete_course_success(self, client, mock_delete_course_use_case):
        """코스 삭제 성공 테스트"""
        course_id = uuid4()
        response_dto = CourseDeleteResponseDTO(success=True, course_id=course_id)
        mock_delete_course_use_case.execute.return_value = response_dto

        # 의존성 오버라이드
        app.dependency_overrides[
            interface.dependencies.get_delete_course_use_case
        ] = lambda: mock_delete_course_use_case
        
        response = client.delete(f"/api/v1/courses/{course_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

