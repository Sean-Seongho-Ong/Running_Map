"""
SQLAlchemy Database Models

데이터베이스 테이블을 정의하는 SQLAlchemy 모델입니다.
PostGIS를 사용하여 지리 공간 데이터를 저장합니다.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from geoalchemy2 import Geometry
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class CourseModel(Base):
    """
    코스 데이터베이스 모델
    
    Attributes:
        id: 코스 ID (UUID)
        name: 코스 이름
        distance: 코스 거리 (km)
        polyline: 폴리라인 (PostGIS LINESTRING)
        metadata: 메타데이터 (JSONB)
        is_public: 공개 여부
        user_id: 사용자 ID (향후 구현)
        created_at: 생성일시
        updated_at: 수정일시
    """

    __tablename__ = "courses"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    distance = Column(Numeric(10, 2), nullable=False)  # km
    polyline = Column(
        Geometry("LINESTRING", srid=4326), nullable=False
    )  # PostGIS LINESTRING
    course_metadata = Column("metadata", JSON, nullable=True)  # JSONB in PostgreSQL
    is_public = Column(Boolean, default=False, nullable=False)
    user_id = Column(
        PostgresUUID(as_uuid=True), nullable=True
    )  # 향후 users 테이블과 연결
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    # 관계 (향후 구현)
    # user = relationship("UserModel", back_populates="courses")
    # running_sessions = relationship("RunningSessionModel", back_populates="course")

    # 인덱스
    __table_args__ = (
        Index("idx_courses_polyline", "polyline", postgresql_using="gist"),
        Index("idx_courses_user_id", "user_id"),
        Index("idx_courses_public", "is_public"),
        Index("idx_courses_distance", "distance"),
    )

    def __repr__(self) -> str:
        return f"<CourseModel(id={self.id}, name={self.name}, distance={self.distance}km)>"


class RunningSessionModel(Base):
    """
    러닝 세션 데이터베이스 모델
    
    Attributes:
        id: 세션 ID (UUID)
        course_id: 사용한 코스 ID (선택사항)
        user_id: 사용자 ID (향후 구현)
        start_time: 시작 시간
        end_time: 종료 시간 (선택사항)
        total_distance: 총 거리 (km)
        total_duration: 총 시간 (초)
        avg_pace: 평균 페이스 (분/km)
        elevation_gain: 누적 상승 고도 (m)
        route_polyline: 러닝 경로 (PostGIS LINESTRING)
        created_at: 생성일시
    """

    __tablename__ = "running_sessions"

    id = Column(PostgresUUID(as_uuid=True), primary_key=True, default=uuid4)
    course_id = Column(
        PostgresUUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="SET NULL"),
        nullable=True,
    )
    user_id = Column(
        PostgresUUID(as_uuid=True), nullable=True
    )  # 향후 users 테이블과 연결
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    total_distance = Column(Numeric(10, 2), nullable=True)  # km
    total_duration = Column(Integer, nullable=True)  # 초
    avg_pace = Column(Numeric(5, 2), nullable=True)  # 분/km
    elevation_gain = Column(Numeric(8, 2), nullable=True)  # m
    route_polyline = Column(
        Geometry("LINESTRING", srid=4326), nullable=True
    )  # PostGIS LINESTRING
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # 관계 (향후 구현)
    # course = relationship("CourseModel", back_populates="running_sessions")
    # user = relationship("UserModel", back_populates="running_sessions")

    # 인덱스
    __table_args__ = (
        Index("idx_running_sessions_user_id", "user_id"),
        Index("idx_running_sessions_course_id", "course_id"),
        Index("idx_running_sessions_start_time", "start_time"),
        Index(
            "idx_running_sessions_route",
            "route_polyline",
            postgresql_using="gist",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<RunningSessionModel(id={self.id}, "
            f"course_id={self.course_id}, "
            f"distance={self.total_distance}km)>"
        )

