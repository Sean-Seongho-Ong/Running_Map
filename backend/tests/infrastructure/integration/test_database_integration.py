"""
Database Integration Tests

실제 PostgreSQL 데이터베이스 연결 및 CRUD 동작을 테스트합니다.
"""

import pytest
from uuid import uuid4

from domain.entities.course import Course, CourseMetadata
from domain.entities.running_session import RunningSession, RunningStats
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.database.repositories.course_repository import CourseRepositoryImpl
from infrastructure.database.repositories.running_session_repository import (
    RunningSessionRepositoryImpl,
)
from infrastructure.database.session import AsyncSessionLocal


@pytest.fixture
async def db_session():
    """실제 데이터베이스 세션"""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        # 테스트 후 롤백 및 세션 정리
        await session.rollback()
        await session.close()


async def get_course_repository():
    """CourseRepository 인스턴스 생성 헬퍼"""
    session = AsyncSessionLocal()
    return CourseRepositoryImpl(session), session


async def get_running_session_repository():
    """RunningSessionRepository 인스턴스 생성 헬퍼"""
    session = AsyncSessionLocal()
    return RunningSessionRepositoryImpl(session), session


@pytest.mark.asyncio
@pytest.mark.integration
class TestDatabaseConnection:
    """데이터베이스 연결 테스트"""

    async def test_database_connection(self):
        """데이터베이스 연결 확인"""
        from sqlalchemy import text

        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1

    async def test_postgis_extension(self):
        """PostGIS 확장 확인"""
        from sqlalchemy import text

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                text("SELECT EXISTS(SELECT 1 FROM pg_extension WHERE extname = 'postgis')")
            )
            assert result.scalar() is True

    async def test_tables_exist(self):
        """테이블 존재 확인"""
        from sqlalchemy import text

        async with AsyncSessionLocal() as session:
            # courses 테이블 확인
            result = await session.execute(
                text(
                    "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'courses')"
                )
            )
            assert result.scalar() is True

            # running_sessions 테이블 확인
            result = await session.execute(
                text(
                    "SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'running_sessions')"
                )
            )
            assert result.scalar() is True


@pytest.mark.asyncio
@pytest.mark.integration
class TestCourseRepositoryIntegration:
    """CourseRepository 통합 테스트"""

    async def test_create_course(self):
        """코스 생성 테스트"""
        repository, session = await get_course_repository()
        try:
            polyline = [
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
                Coordinate(latitude=37.5675, longitude=126.9790),
            ]

            course = Course(
                name="통합 테스트 코스",
                polyline=polyline,
                distance=Distance.from_kilometers(5.0),
                metadata=CourseMetadata(estimated_time=30),
            )

            created_course = await repository.create(course)
            await session.commit()

            assert created_course.id is not None
            assert created_course.name == "통합 테스트 코스"
            assert len(created_course.polyline) == 3
            assert created_course.distance.kilometers == 5.0

            # 정리
            await repository.delete(created_course.id)
            await session.commit()
        finally:
            await session.close()

    async def test_get_course_by_id(self):
        """코스 ID로 조회 테스트"""
        repository, session = await get_course_repository()
        try:
            # 먼저 코스 생성
            polyline = [
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
            ]

            course = Course(
                name="조회 테스트 코스",
                polyline=polyline,
                distance=Distance.from_kilometers(3.0),
            )

            created_course = await repository.create(course)
            await session.commit()
            course_id = created_course.id

            # 조회
            retrieved_course = await repository.get_by_id(course_id)

            assert retrieved_course is not None
            assert retrieved_course.id == course_id
            assert retrieved_course.name == "조회 테스트 코스"
            assert len(retrieved_course.polyline) == 2

            # 정리
            await repository.delete(course_id)
            await session.commit()
        finally:
            await session.close()

    async def test_list_courses(self):
        """코스 목록 조회 테스트"""
        repository, session = await get_course_repository()
        try:
            # 여러 코스 생성
            created_ids = []
            for i in range(3):
                polyline = [
                    Coordinate(latitude=37.5665 + i * 0.001, longitude=126.9780 + i * 0.001),
                    Coordinate(latitude=37.5670 + i * 0.001, longitude=126.9785 + i * 0.001),
                ]

                course = Course(
                    name=f"목록 테스트 코스 {i+1}",
                    polyline=polyline,
                    distance=Distance.from_kilometers(2.0 + i),
                )
                created = await repository.create(course)
                created_ids.append(created.id)
            await session.commit()

            # 목록 조회
            courses = await repository.list(limit=10)

            # 생성한 코스가 목록에 있는지 확인
            course_names = [c.name for c in courses]
            assert any("목록 테스트 코스" in name for name in course_names)

            # 정리
            for course_id in created_ids:
                await repository.delete(course_id)
            await session.commit()
        finally:
            await session.close()

    async def test_update_course(self):
        """코스 업데이트 테스트"""
        repository, session = await get_course_repository()
        try:
            # 코스 생성
            polyline = [
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
            ]

            course = Course(
                name="업데이트 전 코스",
                polyline=polyline,
                distance=Distance.from_kilometers(4.0),
            )

            created_course = await repository.create(course)
            await session.commit()

            # 업데이트
            created_course.name = "업데이트 후 코스"
            updated_course = await repository.update(created_course)
            await session.commit()

            assert updated_course.name == "업데이트 후 코스"
            assert updated_course.id == created_course.id

            # 정리
            await repository.delete(created_course.id)
            await session.commit()
        finally:
            await session.close()

    async def test_delete_course(self):
        """코스 삭제 테스트"""
        repository, session = await get_course_repository()
        try:
            # 코스 생성
            polyline = [
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
            ]

            course = Course(
                name="삭제 테스트 코스",
                polyline=polyline,
                distance=Distance.from_kilometers(1.0),
            )

            created_course = await repository.create(course)
            await session.commit()
            course_id = created_course.id

            # 삭제
            deleted = await repository.delete(course_id)
            await session.commit()
            assert deleted is True

            # 삭제 확인
            retrieved_course = await repository.get_by_id(course_id)
            assert retrieved_course is None
        finally:
            await session.close()


@pytest.mark.asyncio
@pytest.mark.integration
class TestRunningSessionRepositoryIntegration:
    """RunningSessionRepository 통합 테스트"""

    async def test_create_running_session(self):
        """러닝 세션 생성 테스트"""
        repository, session = await get_running_session_repository()
        try:
            start_location = Coordinate(latitude=37.5665, longitude=126.9780)
            route = [
                start_location,
                Coordinate(latitude=37.5670, longitude=126.9785),
                Coordinate(latitude=37.5675, longitude=126.9790),
            ]

            running_session = RunningSession(
                start_location=start_location,
                route=route,
                stats=RunningStats(
                    distance=Distance.from_kilometers(3.0),
                    duration=1800,  # 30분
                    pace=10.0,
                ),
            )

            created_session = await repository.create(running_session)
            await session.commit()

            assert created_session.id is not None
            assert created_session.start_location.latitude == 37.5665
            assert len(created_session.route) == 3
            assert created_session.stats.distance.kilometers == 3.0
        finally:
            await session.close()

    async def test_get_running_session_by_id(self):
        """러닝 세션 ID로 조회 테스트"""
        repository, session = await get_running_session_repository()
        try:
            # 세션 생성
            start_location = Coordinate(latitude=37.5665, longitude=126.9780)
            route = [start_location]

            running_session = RunningSession(
                start_location=start_location,
                route=route,
                stats=RunningStats(distance=Distance.from_kilometers(2.0)),
            )

            created_session = await repository.create(running_session)
            await session.commit()
            session_id = created_session.id

            # 조회
            retrieved_session = await repository.get_by_id(session_id)

            assert retrieved_session is not None
            assert retrieved_session.id == session_id
            assert retrieved_session.start_location.latitude == 37.5665
        finally:
            await session.close()

    async def test_update_running_session(self):
        """러닝 세션 업데이트 테스트"""
        repository, session = await get_running_session_repository()
        try:
            # 세션 생성
            start_location = Coordinate(latitude=37.5665, longitude=126.9780)
            route = [start_location]

            running_session = RunningSession(
                start_location=start_location,
                route=route,
                stats=RunningStats(distance=Distance.from_kilometers(1.0)),
            )

            created_session = await repository.create(running_session)
            await session.commit()

            # 업데이트
            created_session.stats.distance = Distance.from_kilometers(5.0)
            created_session.stats.duration = 3600

            updated_session = await repository.update(created_session)
            await session.commit()

            assert updated_session.stats.distance.kilometers == 5.0
            assert updated_session.stats.duration == 3600
        finally:
            await session.close()


@pytest.mark.asyncio
@pytest.mark.integration
class TestPostGISIntegration:
    """PostGIS 기능 통합 테스트"""

    async def test_linestring_storage(self):
        """LINESTRING 저장 및 조회 테스트"""
        repository, session = await get_course_repository()
        try:
            polyline = [
                Coordinate(latitude=37.5665, longitude=126.9780),
                Coordinate(latitude=37.5670, longitude=126.9785),
                Coordinate(latitude=37.5675, longitude=126.9790),
            ]

            course = Course(
                name="PostGIS 테스트 코스",
                polyline=polyline,
                distance=Distance.from_kilometers(5.0),
            )

            created_course = await repository.create(course)
            await session.commit()

            # 조회하여 좌표 확인
            retrieved_course = await repository.get_by_id(created_course.id)

            assert retrieved_course is not None
            assert len(retrieved_course.polyline) == 3
            assert retrieved_course.polyline[0].latitude == 37.5665
            assert retrieved_course.polyline[0].longitude == 126.9780

            # 정리
            await repository.delete(created_course.id)
            await session.commit()
        finally:
            await session.close()

    async def test_spatial_index(self):
        """공간 인덱스 확인"""
        from sqlalchemy import text

        async with AsyncSessionLocal() as session:
            # courses 테이블의 polyline 인덱스 확인
            result = await session.execute(
                text(
                    """
                    SELECT EXISTS(
                        SELECT 1 FROM pg_indexes 
                        WHERE tablename = 'courses' 
                        AND indexname = 'idx_courses_polyline'
                    )
                    """
                )
            )
            assert result.scalar() is True

            # running_sessions 테이블의 route_polyline 인덱스 확인
            result = await session.execute(
                text(
                    """
                    SELECT EXISTS(
                        SELECT 1 FROM pg_indexes 
                        WHERE tablename = 'running_sessions' 
                        AND indexname = 'idx_running_sessions_route'
                    )
                    """
                )
            )
            assert result.scalar() is True

