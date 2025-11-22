"""
Running Session Repository Implementation

러닝 세션 리포지토리의 SQLAlchemy 구현입니다.
"""

import logging
from typing import Optional, List
from uuid import UUID

from geoalchemy2 import WKTElement
from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities.running_session import RunningSession, RunningSegment, RunningStats
from domain.repositories.running_session_repository import RunningSessionRepository
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.database.models import RunningSessionModel
from infrastructure.exceptions import (
    DatabaseError,
    DatabaseConnectionError,
    DatabaseTransactionError,
)

logger = logging.getLogger(__name__)


class RunningSessionRepositoryImpl(RunningSessionRepository):
    """
    러닝 세션 리포지토리 구현
    
    SQLAlchemy를 사용하여 러닝 세션 데이터를 관리합니다.
    """

    def __init__(self, db: AsyncSession):
        """
        Args:
            db: 데이터베이스 세션
        """
        self.db = db

    def _to_entity(self, model: RunningSessionModel) -> RunningSession:
        """
        데이터베이스 모델을 도메인 엔티티로 변환합니다.
        
        Args:
            model: 데이터베이스 모델
            
        Returns:
            도메인 엔티티
        """
        # PostGIS LINESTRING을 좌표 배열로 변환
        route_coords = []
        if model.route_polyline:
            try:
                # shapely를 사용하여 WKB를 파싱
                from shapely import wkb
                
                # WKBElement에서 데이터 추출
                if hasattr(model.route_polyline, 'data'):
                    # 바이너리 데이터
                    geom = wkb.loads(model.route_polyline.data)
                elif hasattr(model.route_polyline, 'desc'):
                    # 16진수 문자열인 경우
                    import binascii
                    wkb_data = binascii.unhexlify(model.route_polyline.desc)
                    geom = wkb.loads(wkb_data)
                else:
                    # 직접 WKB 데이터
                    geom = wkb.loads(bytes(model.route_polyline))
                
                # shapely geometry에서 좌표 추출
                if hasattr(geom, 'coords'):
                    for lon, lat in geom.coords:
                        route_coords.append(Coordinate(latitude=lat, longitude=lon))
                else:
                    # WKT로 변환 후 파싱
                    wkt_str = geom.wkt
                    if wkt_str.startswith("LINESTRING"):
                        coords_str = wkt_str.replace("LINESTRING", "").strip("()")
                        for coord_str in coords_str.split(","):
                            lon, lat = map(float, coord_str.strip().split())
                            route_coords.append(Coordinate(latitude=lat, longitude=lon))
            except Exception as e:
                logger.error(f"route_polyline 변환 실패: {e}")
                route_coords = []

        # 시작 위치는 첫 번째 좌표 또는 기본값
        start_location = route_coords[0] if route_coords else Coordinate(
            latitude=0.0, longitude=0.0
        )
        end_location = route_coords[-1] if len(route_coords) > 1 else None

        # 통계 정보 생성
        stats = RunningStats(
            distance=Distance.from_kilometers(float(model.total_distance or 0.0)),
            duration=model.total_duration or 0,
            pace=float(model.avg_pace or 0.0),
            elevation_gain=float(model.elevation_gain or 0.0),
        )
        stats.update_speed()

        return RunningSession(
            id=model.id,
            course_id=model.course_id,
            start_location=start_location,
            end_location=end_location,
            route=route_coords,
            stats=stats,
            started_at=model.start_time,
            finished_at=model.end_time,
        )

    def _to_model(self, entity: RunningSession) -> RunningSessionModel:
        """
        도메인 엔티티를 데이터베이스 모델로 변환합니다.
        
        Args:
            entity: 도메인 엔티티
            
        Returns:
            데이터베이스 모델
        """
        # 좌표 배열을 PostGIS LINESTRING으로 변환
        route_polyline_geom = None
        if entity.route and len(entity.route) > 1:
            coords_wkt = ", ".join(
                [f"{coord.longitude} {coord.latitude}" for coord in entity.route]
            )
            linestring_wkt = f"LINESTRING({coords_wkt})"
            route_polyline_geom = WKTElement(linestring_wkt, srid=4326)

        return RunningSessionModel(
            id=entity.id,
            course_id=entity.course_id,
            start_time=entity.started_at,
            end_time=entity.finished_at,
            total_distance=entity.stats.distance.kilometers,
            total_duration=entity.stats.duration,
            avg_pace=entity.stats.pace,
            elevation_gain=entity.stats.elevation_gain,
            route_polyline=route_polyline_geom,
        )

    async def create(self, session: RunningSession) -> RunningSession:
        """러닝 세션을 생성합니다."""
        try:
            model = self._to_model(session)
            self.db.add(model)
            await self.db.commit()
            await self.db.refresh(model)
            return self._to_entity(model)
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 생성 실패 - 무결성 오류: {e}")
            raise DatabaseError(f"러닝 세션 생성 실패: 무결성 제약 조건 위반") from e
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 생성 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 생성 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def get_by_id(
        self,
        session_id: UUID,
        load_relationships: bool = False,
        select_fields: Optional[List[str]] = None,
    ) -> Optional[RunningSession]:
        """
        ID로 러닝 세션을 조회합니다.
        
        Args:
            session_id: 세션 ID
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
                field_map = {
                    "id": RunningSessionModel.id,
                    "course_id": RunningSessionModel.course_id,
                    "start_time": RunningSessionModel.start_time,
                    "end_time": RunningSessionModel.end_time,
                    "route_polyline": RunningSessionModel.route_polyline,
                    "total_distance": RunningSessionModel.total_distance,
                    "total_duration": RunningSessionModel.total_duration,
                    "avg_pace": RunningSessionModel.avg_pace,
                    "elevation_gain": RunningSessionModel.elevation_gain,
                }
                fields = [field_map[f] for f in select_fields if f in field_map]
                if fields:
                    query = select(*fields).where(RunningSessionModel.id == session_id)
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
                    model = RunningSessionModel(
                        id=model_dict.get("id", session_id),
                        course_id=model_dict.get("course_id"),
                        start_time=model_dict.get("start_time"),
                        end_time=model_dict.get("end_time"),
                        route_polyline=model_dict.get("route_polyline"),
                        total_distance=model_dict.get("total_distance"),
                        total_duration=model_dict.get("total_duration"),
                        avg_pace=model_dict.get("avg_pace"),
                        elevation_gain=model_dict.get("elevation_gain"),
                    )
                else:
                    query = select(RunningSessionModel).where(RunningSessionModel.id == session_id)
                    result = await self.db.execute(query)
                    model = result.scalar_one_or_none()
                    if model is None:
                        return None
            else:
                # 모든 필드 선택
                query = select(RunningSessionModel).where(RunningSessionModel.id == session_id)
                
                # Eager loading (향후 관계 추가 시 사용)
                # 예: query = query.options(selectinload(RunningSessionModel.course))
                
                result = await self.db.execute(query)
                model = result.scalar_one_or_none()
                if model is None:
                    return None
            
            return self._to_entity(model)
        except OperationalError as e:
            logger.error(f"러닝 세션 조회 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            logger.error(f"러닝 세션 조회 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

    async def update(self, session: RunningSession) -> RunningSession:
        """러닝 세션을 업데이트합니다."""
        try:
            # 좌표 배열을 PostGIS LINESTRING으로 변환
            route_polyline_geom = None
            if session.route and len(session.route) > 1:
                coords_wkt = ", ".join(
                    [f"{coord.longitude} {coord.latitude}" for coord in session.route]
                )
                linestring_wkt = f"LINESTRING({coords_wkt})"
                route_polyline_geom = WKTElement(linestring_wkt, srid=4326)

            await self.db.execute(
                update(RunningSessionModel)
                .where(RunningSessionModel.id == session.id)
                .values(
                    course_id=session.course_id,
                    start_time=session.started_at,
                    end_time=session.finished_at,
                    total_distance=session.stats.distance.kilometers,
                    total_duration=session.stats.duration,
                    avg_pace=session.stats.pace,
                    elevation_gain=session.stats.elevation_gain,
                    route_polyline=route_polyline_geom,
                )
            )
            await self.db.commit()

            # 업데이트된 모델 조회
            return await self.get_by_id(session.id)
        except IntegrityError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 업데이트 실패 - 무결성 오류: {e}")
            raise DatabaseError(f"러닝 세션 업데이트 실패: 무결성 제약 조건 위반") from e
        except OperationalError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 업데이트 실패 - 데이터베이스 연결 오류: {e}")
            raise DatabaseConnectionError(f"데이터베이스 연결 오류: {str(e)}") from e
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"러닝 세션 업데이트 실패 - 데이터베이스 오류: {e}")
            raise DatabaseError(f"데이터베이스 오류: {str(e)}") from e

