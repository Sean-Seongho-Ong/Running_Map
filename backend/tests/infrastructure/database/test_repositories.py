"""
Repository Tests

리포지토리 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

from domain.entities.course import Course, CourseMetadata
from domain.entities.running_session import RunningSession, RunningStats
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.database.models import CourseModel, RunningSessionModel
from infrastructure.database.repositories.course_repository import CourseRepositoryImpl
from infrastructure.database.repositories.running_session_repository import (
    RunningSessionRepositoryImpl,
)
from infrastructure.exceptions import DatabaseError, DatabaseConnectionError


class TestCourseRepository:
    """CourseRepository 테스트"""

    @pytest.fixture
    def repository(self, mock_db_session):
        """CourseRepository 인스턴스"""
        return CourseRepositoryImpl(mock_db_session)

    @pytest.fixture
    def sample_course_model(self):
        """샘플 CourseModel"""
        model = CourseModel(
            id=uuid4(),
            name="테스트 코스",
            distance=10.0,
            polyline="LINESTRING(126.9780 37.5665, 126.9785 37.5670)",
            metadata={"estimated_time": 60},
            is_public=False,
        )
        return model

    @pytest.mark.asyncio
    async def test_create_success(self, repository, sample_course, mock_db_session):
        """코스 생성 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()

        # 실행
        result = await repository.create(sample_course)

        # 검증
        assert result.name == sample_course.name
        assert mock_db_session.add.called
        assert mock_db_session.commit.called

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, repository, sample_course_model, mock_db_session
    ):
        """코스 ID로 조회 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_course_model
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.get_by_id(sample_course_model.id)

        # 검증
        assert result is not None
        assert result.name == sample_course_model.name

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository, mock_db_session):
        """코스 ID로 조회 - 없음 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.get_by_id(uuid4())

        # 검증
        assert result is None

    @pytest.mark.asyncio
    async def test_list_success(self, repository, sample_course_model, mock_db_session):
        """코스 목록 조회 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = [sample_course_model]
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.list(limit=10, offset=0)

        # 검증
        assert len(result) == 1
        assert result[0].name == sample_course_model.name

    @pytest.mark.asyncio
    async def test_update_success(self, repository, sample_course, mock_db_session):
        """코스 업데이트 성공 테스트"""
        # Mock 설정
        from geoalchemy2 import WKTElement
        from domain.value_objects.coordinate import Coordinate
        
        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_model.id = sample_course.id
        mock_model.name = "업데이트된 코스"
        mock_model.course_metadata = None
        mock_model.distance = 10.0
        # WKTElement로 polyline 설정 (실제 리포지토리에서 사용하는 형식)
        mock_model.polyline = WKTElement(
            "LINESTRING(126.9780 37.5665, 126.9785 37.5670, 126.9790 37.5675)",
            srid=4326
        )
        mock_model.is_public = False
        mock_model.user_id = None
        mock_model.created_at = None
        mock_model.updated_at = None

        # execute를 두 번 호출 (update와 get_by_id)
        # 첫 번째는 update, 두 번째는 get_by_id
        call_count = 0
        async def execute_side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                # update 실행
                return MagicMock()
            else:
                # get_by_id 실행
                mock_result.scalar_one_or_none.return_value = mock_model
                return mock_result
        
        mock_db_session.execute = AsyncMock(side_effect=execute_side_effect)
        mock_db_session.commit = AsyncMock()

        # 실행
        sample_course.name = "업데이트된 코스"
        result = await repository.update(sample_course)

        # 검증
        assert mock_db_session.commit.called
        assert call_count == 2  # update와 get_by_id
        assert result.name == "업데이트된 코스"

    @pytest.mark.asyncio
    async def test_delete_success(self, repository, sample_course_model, mock_db_session):
        """코스 삭제 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_course_model
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        mock_db_session.delete = AsyncMock()
        mock_db_session.commit = AsyncMock()

        # 실행
        result = await repository.delete(sample_course_model.id)

        # 검증
        assert result is True
        assert mock_db_session.delete.called
        assert mock_db_session.commit.called

    @pytest.mark.asyncio
    async def test_delete_not_found(self, repository, mock_db_session):
        """코스 삭제 - 없음 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.delete(uuid4())

        # 검증
        assert result is False


class TestRunningSessionRepository:
    """RunningSessionRepository 테스트"""

    @pytest.fixture
    def repository(self, mock_db_session):
        """RunningSessionRepository 인스턴스"""
        return RunningSessionRepositoryImpl(mock_db_session)

    @pytest.fixture
    def sample_session_model(self):
        """샘플 RunningSessionModel"""
        model = RunningSessionModel(
            id=uuid4(),
            start_time=None,
            total_distance=5.0,
            total_duration=1800,
            avg_pace=6.0,
            elevation_gain=50.0,
        )
        return model

    @pytest.mark.asyncio
    async def test_create_success(
        self, repository, sample_running_session, mock_db_session
    ):
        """러닝 세션 생성 성공 테스트"""
        from geoalchemy2 import WKTElement
        from domain.value_objects.coordinate import Coordinate
        
        # Mock 설정
        mock_db_session.add = MagicMock()
        mock_db_session.commit = AsyncMock()
        mock_db_session.refresh = AsyncMock()
        
        # refresh 후 모델이 반환되도록 설정
        # route_polyline을 설정하여 start_location이 제대로 추출되도록 함
        start_coord = sample_running_session.start_location
        route_polyline_wkt = WKTElement(
            f"LINESTRING({start_coord.longitude} {start_coord.latitude}, {start_coord.longitude + 0.001} {start_coord.latitude + 0.001})",
            srid=4326
        )
        
        mock_model = MagicMock()
        mock_model.id = sample_running_session.id
        mock_model.course_id = None
        mock_model.start_time = sample_running_session.started_at
        mock_model.end_time = None
        mock_model.total_distance = sample_running_session.stats.distance.kilometers
        mock_model.total_duration = sample_running_session.stats.duration
        mock_model.avg_pace = sample_running_session.stats.pace
        mock_model.elevation_gain = sample_running_session.stats.elevation_gain
        mock_model.route_polyline = route_polyline_wkt
        mock_model.created_at = None
        
        # refresh가 모델을 반환하도록 설정
        def refresh_side_effect(model):
            # 모델 속성 설정
            for attr, value in vars(mock_model).items():
                if not attr.startswith('_'):
                    setattr(model, attr, value)
        
        mock_db_session.refresh.side_effect = refresh_side_effect

        # 실행
        result = await repository.create(sample_running_session)

        # 검증
        assert result.start_location.latitude == start_coord.latitude
        assert result.start_location.longitude == start_coord.longitude
        assert mock_db_session.add.called
        assert mock_db_session.commit.called

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self, repository, sample_session_model, mock_db_session
    ):
        """러닝 세션 ID로 조회 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_session_model
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.get_by_id(sample_session_model.id)

        # 검증
        assert result is not None
        assert result.stats.distance.kilometers == float(sample_session_model.total_distance)

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository, mock_db_session):
        """러닝 세션 ID로 조회 - 없음 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_db_session.execute = AsyncMock(return_value=mock_result)

        # 실행
        result = await repository.get_by_id(uuid4())

        # 검증
        assert result is None

    @pytest.mark.asyncio
    async def test_update_success(
        self, repository, sample_running_session, mock_db_session
    ):
        """러닝 세션 업데이트 성공 테스트"""
        # Mock 설정
        mock_result = MagicMock()
        mock_model = MagicMock()
        mock_model.id = sample_running_session.id
        mock_model.course_id = None
        mock_model.start_time = None
        mock_model.end_time = None
        mock_model.total_distance = 5.0
        mock_model.total_duration = 1800
        mock_model.avg_pace = 6.0
        mock_model.elevation_gain = 50.0
        mock_model.route_polyline = None
        mock_model.created_at = None

        mock_result.scalar_one_or_none.return_value = mock_model
        mock_db_session.execute = AsyncMock(return_value=mock_result)
        mock_db_session.commit = AsyncMock()

        # 실행
        result = await repository.update(sample_running_session)

        # 검증
        assert mock_db_session.commit.called

