"""
OSRM Client

OSRM (Open Source Routing Machine) API 클라이언트입니다.
"""

import asyncio
import logging
from typing import Optional

import httpx

from domain.services.route_calculator import RouteCalculator, RouteCalculationError
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.config.settings import settings
from infrastructure.exceptions import (
    ExternalServiceError,
    ExternalServiceTimeoutError,
    ExternalServiceRateLimitError,
)

logger = logging.getLogger(__name__)


class OSRMClient(RouteCalculator):
    """
    OSRM 클라이언트 구현
    
    OSRM API를 사용하여 경로 계산을 수행합니다.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        """
        Args:
            base_url: OSRM 서버 URL (기본값: settings.OSRM_BASE_URL)
            timeout: 요청 타임아웃 (초)
            max_retries: 최대 재시도 횟수
            retry_delay: 재시도 지연 시간 (초, exponential backoff의 초기값)
        """
        self.base_url = base_url or settings.OSRM_BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.client = httpx.AsyncClient(
            timeout=timeout,
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

    def _coordinate_to_osrm_format(self, coord: Coordinate) -> str:
        """
        좌표를 OSRM 형식으로 변환합니다.
        
        Args:
            coord: 좌표
            
        Returns:
            OSRM 형식 문자열 (경도,위도)
        """
        # 소수점 6자리까지 표시 (OSRM 권장 형식)
        return f"{coord.longitude:.6f},{coord.latitude:.6f}"

    def _osrm_profile_to_path(self, profile: str) -> str:
        """
        프로파일을 OSRM 경로로 변환합니다.
        
        Args:
            profile: 프로파일 (foot, bike, car)
            
        Returns:
            OSRM 경로 (foot, cycling, driving)
        """
        profile_map = {
            "foot": "foot",
            "bike": "cycling",
            "car": "driving",
        }
        return profile_map.get(profile, "foot")

    async def _make_request_with_retry(
        self,
        url: str,
        params: dict,
        operation_name: str = "request",
    ) -> httpx.Response:
        """
        재시도 로직이 포함된 HTTP 요청을 수행합니다.
        
        Args:
            url: 요청 URL
            params: 요청 파라미터
            operation_name: 작업 이름 (로깅용)
            
        Returns:
            HTTP 응답
            
        Raises:
            ExternalServiceTimeoutError: 타임아웃 오류
            ExternalServiceRateLimitError: Rate Limit 오류
            ExternalServiceError: 기타 외부 서비스 오류
        """
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.get(url, params=params)
                
                # Rate Limit 처리 (429 Too Many Requests)
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", self.retry_delay))
                    if attempt < self.max_retries:
                        logger.warning(
                            f"Rate limit 도달 (attempt {attempt + 1}/{self.max_retries + 1}), "
                            f"{retry_after}초 후 재시도"
                        )
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        raise ExternalServiceRateLimitError(
                            f"OSRM API rate limit 초과: {response.text}"
                        )
                
                response.raise_for_status()
                return response
                
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self.max_retries:
                    # Exponential backoff: 1초, 2초, 4초...
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"{operation_name} 타임아웃 (attempt {attempt + 1}/{self.max_retries + 1}), "
                        f"{delay}초 후 재시도"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise ExternalServiceTimeoutError(
                        f"OSRM API 타임아웃 (시도 {self.max_retries + 1}회): {str(e)}"
                    ) from e
                    
            except httpx.HTTPStatusError as e:
                # 4xx, 5xx 오류는 재시도하지 않음 (클라이언트 오류 또는 서버 오류)
                if e.response.status_code >= 500 and attempt < self.max_retries:
                    # 5xx 서버 오류는 재시도
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"{operation_name} 서버 오류 {e.response.status_code} "
                        f"(attempt {attempt + 1}/{self.max_retries + 1}), "
                        f"{delay}초 후 재시도"
                    )
                    await asyncio.sleep(delay)
                    last_exception = e
                    continue
                else:
                    raise ExternalServiceError(
                        f"OSRM API 오류 ({e.response.status_code}): {str(e)}"
                    ) from e
                    
            except httpx.RequestError as e:
                # 네트워크 오류는 재시도
                last_exception = e
                if attempt < self.max_retries:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.warning(
                        f"{operation_name} 네트워크 오류 (attempt {attempt + 1}/{self.max_retries + 1}), "
                        f"{delay}초 후 재시도"
                    )
                    await asyncio.sleep(delay)
                else:
                    raise ExternalServiceError(
                        f"OSRM API 네트워크 오류 (시도 {self.max_retries + 1}회): {str(e)}"
                    ) from e
        
        # 모든 재시도 실패
        raise ExternalServiceError(
            f"{operation_name} 실패 (최대 재시도 횟수 초과)"
        ) from last_exception

    async def calculate_route(
        self,
        start: Coordinate,
        end: Coordinate,
        profile: str = "foot",
    ) -> list[Coordinate]:
        """
        두 좌표 간의 경로를 계산합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            profile: 라우팅 프로파일 (foot, bike, car)
            
        Returns:
            경로 좌표 배열
            
        Raises:
            RouteCalculationError: 경로 계산 실패 시
        """
        try:
            # OSRM route API 호출
            osrm_profile = self._osrm_profile_to_path(profile)
            start_str = self._coordinate_to_osrm_format(start)
            end_str = self._coordinate_to_osrm_format(end)

            url = f"{self.base_url}/route/v1/{osrm_profile}/{start_str};{end_str}"
            params = {
                "overview": "full",  # 전체 경로 반환
                "geometries": "geojson",  # GeoJSON 형식
                "steps": "false",  # 단계별 정보 불필요
            }

            # 재시도 로직이 포함된 요청
            response = await self._make_request_with_retry(
                url, params, operation_name="경로 계산"
            )

            data = response.json()

            # 응답 검증
            if data.get("code") != "Ok":
                error_msg = data.get("message", "Unknown error")
                raise RouteCalculationError(f"OSRM API error: {error_msg}")

            # 경로 좌표 추출
            routes = data.get("routes", [])
            if not routes:
                raise RouteCalculationError("No routes found in OSRM response")

            route = routes[0]
            geometry = route.get("geometry", {})
            coordinates = geometry.get("coordinates", [])

            # GeoJSON 형식: [[경도, 위도], ...]
            # Coordinate 객체로 변환
            route_coords = []
            for coord_pair in coordinates:
                lon, lat = coord_pair
                route_coords.append(Coordinate(latitude=lat, longitude=lon))

            logger.info(
                f"Route calculated: {len(route_coords)} points, "
                f"distance: {route.get('distance', 0) / 1000:.2f}km"
            )

            return route_coords

        except (ExternalServiceError, ExternalServiceTimeoutError, ExternalServiceRateLimitError) as e:
            # 인프라 예외를 도메인 예외로 변환
            raise RouteCalculationError(f"경로 계산 실패: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error during route calculation: {e}")
            raise RouteCalculationError(f"Unexpected error: {str(e)}") from e

    async def calculate_distance(
        self,
        start: Coordinate,
        end: Coordinate,
        profile: str = "foot",
    ) -> Distance:
        """
        두 좌표 간의 거리를 계산합니다.
        
        Args:
            start: 시작 좌표
            end: 종료 좌표
            profile: 라우팅 프로파일 (foot, bike, car)
            
        Returns:
            거리
            
        Raises:
            RouteCalculationError: 거리 계산 실패 시
        """
        try:
            # OSRM route API 호출 (거리만 필요)
            osrm_profile = self._osrm_profile_to_path(profile)
            start_str = self._coordinate_to_osrm_format(start)
            end_str = self._coordinate_to_osrm_format(end)

            url = f"{self.base_url}/route/v1/{osrm_profile}/{start_str};{end_str}"
            params = {
                "overview": "false",  # 경로 정보 불필요
            }

            # 재시도 로직이 포함된 요청
            response = await self._make_request_with_retry(
                url, params, operation_name="거리 계산"
            )

            data = response.json()

            # 응답 검증
            if data.get("code") != "Ok":
                error_msg = data.get("message", "Unknown error")
                raise RouteCalculationError(f"OSRM API error: {error_msg}")

            # 거리 추출 (미터 단위)
            routes = data.get("routes", [])
            if not routes:
                raise RouteCalculationError("No routes found in OSRM response")

            route = routes[0]
            distance_meters = route.get("distance", 0)

            # 미터를 킬로미터로 변환
            distance_km = distance_meters / 1000.0

            logger.info(
                f"Distance calculated: {distance_km:.2f}km "
                f"({start} -> {end})"
            )

            return Distance.from_kilometers(distance_km)

        except (ExternalServiceError, ExternalServiceTimeoutError, ExternalServiceRateLimitError) as e:
            # 인프라 예외를 도메인 예외로 변환
            raise RouteCalculationError(f"거리 계산 실패: {str(e)}") from e
        except Exception as e:
            logger.error(f"Unexpected error during distance calculation: {e}")
            raise RouteCalculationError(f"Unexpected error: {str(e)}") from e

    async def close(self) -> None:
        """클라이언트 연결 종료"""
        await self.client.aclose()

