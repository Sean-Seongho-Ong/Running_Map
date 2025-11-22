"""
Course Repository Implementation

코스 리포지토리의 SQLAlchemy 구현입니다.
"""

import logging
from typing import Optional, List
from uuid import UUID

from geoalchemy2 import WKTElement
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.course import Course, CourseMetadata
from domain.repositories.course_repository import CourseRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.database.models import CourseModel
from infrastructure.exceptions import (
    DatabaseError,
    DatabaseConnectionError,
    DatabaseTransactionError,
)

logger = logging.getLogger(__name__)


class CourseRepositoryImpl(CourseRepository):
    """
    코스 리포지토리 구현
    
    SQLAlchemy를 사용하여 코스 데이터를 관리합니다.
    """

    def __init__(self, db: AsyncSession):
        """
        Args:
            db: 데이터베이스 세션
        """
        self.db = db

    def _to_entity(self, model: CourseModel) -> Course:
        """
        데이터베이스 모델을 도메인 엔티티로 변환합니다.
        
        Args:
            model: 데이터베이스 모델
            
        Returns:
            도메인 엔티티
        """
        # PostGIS LINESTRING을 좌표 배열로 변환
        polyline_coords = []
        if model.polyline:
            try:
                # shapely를 사용하여 WKB를 파싱
                from shapely import wkb
                
                # WKBElement에서 데이터 추출
                if hasattr(model.polyline, 'data'):
                    # 바이너리 데이터
                    geom = wkb.loads(model.polyline.data)
                elif hasattr(model.polyline, 'desc'):
                    # 16진수 문자열인 경우
                    import binascii
                    wkb_data = binascii.unhexlify(model.polyline.desc)
                    geom = wkb.loads(wkb_data)
                else:
                    # 직접 WKB 데이터
                    geom = wkb.loads(bytes(model.polyline))
                
                # shapely geometry에서 좌표 추출
                if hasattr(geom, 'coords'):
                    for lon, lat in geom.coords:
                        polyline_coords.append(Coordinate(latitude=lat, longitude=lon))
                else:
                    # WKT로 변환 후 파싱
                    wkt_str = geom.wkt
                    if wkt_str.startswith("LINESTRING"):
                        coords_str = wkt_str.replace("LINESTRING", "").strip("()")
                        for coord_str in coords_str.split(","):
                            lon, lat = map(float, coord_str.strip().split())
                            polyline_coords.append(Coordinate(latitude=lat, longitude=lon))
            except Exception as e:
                logger.error(f"polyline 변환 실패: {e}")
                # 빈 배열 반환 (최소 2개 좌표 필요)
                polyline_coords = []

        # 메타데이터 변환
        metadata = CourseMetadata()
        if model.course_metadata:
            metadata_dict = model.course_metadata
            metadata.estimated_time = metadata_dict.get("estimated_time")
            metadata.elevation_gain = metadata_dict.get("elevation_gain")
            metadata.elevation_loss = metadata_dict.get("elevation_loss")
            metadata.quality_score = metadata_dict.get("quality_score")
            metadata.self_intersections = metadata_dict.get("self_intersections")
            metadata.tags = metadata_dict.get("tags", [])
            metadata.difficulty = metadata_dict.get("difficulty")

        return Course(
            id=model.id,
            name=model.name,
            polyline=polyline_coords,
            distance=Distance.from_kilometers(float(model.distance)),
            metadata=metadata,
            is_public=model.is_public,
            user_id=model.user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: Course) -> CourseModel:
        """
        도메인 엔티티를 데이터베이스 모델로 변환합니다.
        
        Args:
            entity: 도메인 엔티티
            
        Returns:
            데이터베이스 모델
        """
        # 좌표 배열을 PostGIS LINESTRING으로 변환
        coords_wkt = ", ".join(
            [f"{coord.longitude} {coord.latitude}" for coord in entity.polyline]
        )
        linestring_wkt = f"LINESTRING({coords_wkt})"
        polyline_geom = WKTElement(linestring_wkt, srid=4326)

        # 메타데이터 변환
        metadata_dict = None
        if entity.metadata:
            metadata_dict = {
                "estimated_time": entity.metadata.estimated_time,
                "elevation_gain": entity.metadata.elevation_gain,
                "elevation_loss": entity.metadata.elevation_loss,
                "quality_score": entity.metadata.quality_score,
                "self_intersections": entity.metadata.self_intersections,
                "tags": entity.metadata.tags,
                "difficulty": entity.metadata.difficulty,
            }

        return CourseModel(
            id=entity.id,
            name=entity.name,
            distance=entity.distance.kilometers,
            polyline=polyline_geom,
            metadata=metadata_dict,
            is_public=entity.is_public,
            user_id=entity.user_id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    async def create(self, course: Course) -> Course:
        """코스를 생성합니다."""
        try:
            model = self._to_model(course)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return self._to_entity(model)
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"코스 생성 실패 - 무결성 오류: {e}")
            raise DatabaseError(f"코스 생성 실패: 무결성 제약 조건 위반") from e
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"코스 생성 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"코스 생성 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def get_by_id(
        self,
        course_id: UUID,
        load_relationships: bool = False,
        select_fields: Optional[List[str]] = None,
    ) -> Optional[Course]:
        """
        ID로 코스를 조회합니다.
        
        Args:
            course_id: 코스 ID
            load_relationships: 관계 데이터를 eager loading할지 여부 (향후 관계 추가 시 사용)
            select_fields: 선택할 필드 목록 (None이면 모든 필드 선택)
        
        최적화:
        - 인덱스를 활용한 빠른 조회 (id는 기본 키)
        - 필요한 필드만 선택하여 메모리 사용량 감소
        - Eager loading으로 N+1 문제 방지
        """
        try:
            # 필요한 필드만 선택
            if select_fields:
                # 특정 필드만 선택하는 쿼리
                fields = []
                field_map = {
                    "id": CourseModel.id,
                    "name": CourseModel.name,
                    "polyline": CourseModel.polyline,
                    "distance": CourseModel.distance,
                    "metadata": CourseModel.course_metadata,
                    "is_public": CourseModel.is_public,
                    "user_id": CourseModel.user_id,
                    "created_at": CourseModel.created_at,
                    "updated_at": CourseModel.updated_at,
                }
                for field_name in select_fields:
                    if field_name in field_map:
                        fields.append(field_map[field_name])
                
                if fields:
                    query = select(*fields).where(CourseModel.id == course_id)
                    result = await self.db.execute(query)
                    row = result.first()
                    if row is None:
                        return None
                    # Row 객체를 모델로 변환
                    model_dict = {}
                    for i, field_name in enumerate(select_fields):
                        if field_name in field_map:
                            model_dict[field_name] = row[i]
                    # 필수 필드가 없으면 기본값 사용
                    model = CourseModel(
                        id=model_dict.get("id", course_id),
                        name=model_dict.get("name", ""),
                        distance=model_dict.get("distance", 0.0),
                        polyline=model_dict.get("polyline"),
                        course_metadata=model_dict.get("metadata"),
                        is_public=model_dict.get("is_public", False),
                        user_id=model_dict.get("user_id"),
                        created_at=model_dict.get("created_at"),
                        updated_at=model_dict.get("updated_at"),
                    )
                else:
                    # 모든 필드 선택
                    query = select(CourseModel).where(CourseModel.id == course_id)
                    result = await self.db.execute(query)
                    model = result.scalar_one_or_none()
                    if model is None:
                        return None
            else:
                # 모든 필드 선택
                query = select(CourseModel).where(CourseModel.id == course_id)
                
                # Eager loading (향후 관계 추가 시 사용)
                # 예: query = select(CourseModel).options(selectinload(CourseModel.running_sessions))
                
                result = await self.db.execute(query)
                model = result.scalar_one_or_none()
                if model is None:
                    return None
            
            return self._to_entity(model)
        except OperationalError as e:
            logger.error(f"코스 조회 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            logger.error(f"코스 조회 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def list(
        self,
        user_id: Optional[UUID] = None,
        is_public: Optional[bool] = None,
        limit: int = 20,
        offset: int = 0,
        load_relationships: bool = False,
        select_fields: Optional[List[str]] = None,
    ) -> list[Course]:
        """
        코스 목록을 조회합니다.
        
        Args:
            user_id: 사용자 ID 필터
            is_public: 공개 여부 필터
            limit: 조회할 최대 개수
            offset: 건너뛸 개수
            load_relationships: 관계 데이터를 eager loading할지 여부 (향후 관계 추가 시 사용)
            select_fields: 선택할 필드 목록 (None이면 모든 필드 선택)
        
        최적화:
        - 인덱스를 활용한 빠른 조회 (user_id, is_public 인덱스 사용)
        - LIMIT/OFFSET을 통한 페이징 처리
        - 필요한 필드만 선택하여 메모리 사용량 감소
        - Eager loading으로 N+1 문제 방지
        """
        try:
            # 필요한 필드만 선택
            if select_fields:
                field_map = {
                    "id": CourseModel.id,
                    "name": CourseModel.name,
                    "polyline": CourseModel.polyline,
                    "distance": CourseModel.distance,
                    "metadata": CourseModel.course_metadata,
                    "is_public": CourseModel.is_public,
                    "user_id": CourseModel.user_id,
                    "created_at": CourseModel.created_at,
                    "updated_at": CourseModel.updated_at,
                }
                fields = [field_map[f] for f in select_fields if f in field_map]
                if fields:
                    query = select(*fields)
                else:
                    query = select(CourseModel)
            else:
                query = select(CourseModel)

            if user_id is not None:
                query = query.where(CourseModel.user_id == user_id)
            if is_public is not None:
                query = query.where(CourseModel.is_public == is_public)

            # Eager loading (향후 관계 추가 시 사용)
            # 예: query = query.options(selectinload(CourseModel.running_sessions))

            # 인덱스를 활용한 정렬 및 제한
            query = query.limit(limit).offset(offset).order_by(CourseModel.created_at.desc())

            result = await self.db.execute(query)
            
            if select_fields:
                # Row 객체를 모델로 변환
                rows = result.all()
                models = []
                for row in rows:
                    model_dict = {}
                    for i, field_name in enumerate(select_fields):
                        if field_name in field_map:
                            model_dict[field_name] = row[i]
                    # 필수 필드가 없으면 기본값 사용
                    model = CourseModel(
                        id=model_dict.get("id"),
                        name=model_dict.get("name", ""),
                        distance=model_dict.get("distance", 0.0),
                        polyline=model_dict.get("polyline"),
                        course_metadata=model_dict.get("metadata"),
                        is_public=model_dict.get("is_public", False),
                        user_id=model_dict.get("user_id"),
                        created_at=model_dict.get("created_at"),
                        updated_at=model_dict.get("updated_at"),
                    )
                    models.append(model)
            else:
                models = result.scalars().all()
            
            return [self._to_entity(model) for model in models]
        except OperationalError as e:
            logger.error(f"코스 목록 조회 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            logger.error(f"코스 목록 조회 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def update(self, course: Course) -> Course:
        """코스를 업데이트합니다."""
        try:
            # 좌표 배열을 PostGIS LINESTRING으로 변환
            coords_wkt = ", ".join(
                [f"{coord.longitude} {coord.latitude}" for coord in course.polyline]
            )
            linestring_wkt = f"LINESTRING({coords_wkt})"
            polyline_geom = WKTElement(linestring_wkt, srid=4326)

            # 메타데이터 변환
            metadata_dict = None
            if course.metadata:
                metadata_dict = {
                    "estimated_time": course.metadata.estimated_time,
                    "elevation_gain": course.metadata.elevation_gain,
                    "elevation_loss": course.metadata.elevation_loss,
                    "quality_score": course.metadata.quality_score,
                    "self_intersections": course.metadata.self_intersections,
                    "tags": course.metadata.tags,
                    "difficulty": course.metadata.difficulty,
                }

            # SQLAlchemy 2.0 스타일 업데이트
            stmt = (
                update(CourseModel)
                .where(CourseModel.id == course.id)
                .values(
                    name=course.name,
                    distance=course.distance.kilometers,
                    polyline=polyline_geom,
                    course_metadata=metadata_dict,
                    is_public=course.is_public,
                )
            )
            await self.db.execute(stmt)
            await self.db.commit()

            # 업데이트된 모델 조회
            return await self.get_by_id(course.id)
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 무결성 오류: {e}")
            raise DatabaseError(f"코스 업데이트 실패: 무결성 제약 조건 위반") from e
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 무결성 오류: {e}")
            raise DatabaseError(f"코스 업데이트 실패: 무결성 제약 조건 위반") from e
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"코스 업데이트 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def delete(self, course_id: UUID) -> bool:
        """코스를 삭제합니다."""
        try:
            result = await self.db.execute(
                select(CourseModel).where(CourseModel.id == course_id)
            )
            model = result.scalar_one_or_none()
            if model is None:
                return False

            await self.db.delete(model)
            await self.db.commit()
            return True
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"코스 삭제 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"코스 삭제 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

