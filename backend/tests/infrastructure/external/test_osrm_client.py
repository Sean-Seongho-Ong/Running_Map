"""
OSRM Client Tests

OSRM 클라이언트 단위 테스트입니다.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from infrastructure.external.osrm_client import OSRMClient
from domain.services.route_calculator import RouteCalculationError
from infrastructure.exceptions import (
    ExternalServiceTimeoutError,
    ExternalServiceRateLimitError,
)


class TestOSRMClient:
    """OSRMClient 테스트"""

    @pytest.fixture
    def client(self):
        """OSRMClient 인스턴스"""
        return OSRMClient(base_url="http://localhost:5000", timeout=5, max_retries=2)

    @pytest.fixture
    def sample_start(self):
        """샘플 시작 좌표"""
        return Coordinate(latitude=37.5665, longitude=126.9780)

    @pytest.fixture
    def sample_end(self):
        """샘플 종료 좌표"""
        return Coordinate(latitude=37.5670, longitude=126.9785)

    @pytest.fixture
    def mock_osrm_response(self):
        """Mock OSRM API 응답"""
        return {
            "code": "Ok",
            "routes": [
                {
                    "distance": 1000.0,  # 미터
                    "geometry": {
                        "coordinates": [
                            [126.9780, 37.5665],
                            [126.9785, 37.5670],
                        ]
                    },
                }
            ],
        }

    @pytest.mark.asyncio
    async def test_calculate_route_success(
        self, client, sample_start, sample_end, mock_osrm_response
    ):
        """경로 계산 성공 테스트"""
        # Mock httpx 응답
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_osrm_response
        mock_response.raise_for_status = MagicMock()

        with patch.object(client.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # 실행
            result = await client.calculate_route(sample_start, sample_end)

            # 검증
            assert len(result) == 2
            assert result[0].latitude == 37.5665
            assert result[0].longitude == 126.9780

    @pytest.mark.asyncio
    async def test_calculate_route_api_error(
        self, client, sample_start, sample_end
    ):
        """경로 계산 - API 오류 테스트"""
        # Mock httpx 응답 (오류)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"code": "NoRoute", "message": "No route found"}
        mock_response.raise_for_status = MagicMock()

        with patch.object(client.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # 실행 및 검증
            with pytest.raises(RouteCalculationError):
                await client.calculate_route(sample_start, sample_end)

    @pytest.mark.asyncio
    async def test_calculate_route_timeout(
        self, client, sample_start, sample_end
    ):
        """경로 계산 - 타임아웃 테스트"""
        # Mock httpx 타임아웃 예외
        with patch.object(
            client.client, "get", new_callable=AsyncMock
        ) as mock_get:
            mock_get.side_effect = httpx.TimeoutException("Request timeout")

            # 실행 및 검증
            with pytest.raises(RouteCalculationError):
                await client.calculate_route(sample_start, sample_end)

    @pytest.mark.asyncio
    async def test_calculate_route_rate_limit(
        self, client, sample_start, sample_end
    ):
        """경로 계산 - Rate Limit 테스트"""
        # Mock httpx 429 응답
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "1"}
        mock_response.text = "Too Many Requests"

        with patch.object(client.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # 실행 및 검증
            with pytest.raises(RouteCalculationError):
                await client.calculate_route(sample_start, sample_end)

    @pytest.mark.asyncio
    async def test_calculate_distance_success(
        self, client, sample_start, sample_end, mock_osrm_response
    ):
        """거리 계산 성공 테스트"""
        # Mock httpx 응답
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_osrm_response
        mock_response.raise_for_status = MagicMock()

        with patch.object(client.client, "get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response

            # 실행
            result = await client.calculate_distance(sample_start, sample_end)

            # 검증
            assert result.kilometers == 1.0  # 1000m = 1km

    @pytest.mark.asyncio
    async def test_coordinate_to_osrm_format(self, client, sample_start):
        """좌표를 OSRM 형식으로 변환 테스트"""
        result = client._coordinate_to_osrm_format(sample_start)
        # OSRM 형식: "경도,위도"
        assert "126.978" in result
        assert "37.5665" in result
        assert "," in result
        parts = result.split(",")
        assert len(parts) == 2
        assert float(parts[0]) == 126.9780  # 경도
        assert float(parts[1]) == 37.5665  # 위도

    @pytest.mark.asyncio
    async def test_osrm_profile_to_path(self, client):
        """프로파일을 OSRM 경로로 변환 테스트"""
        assert client._osrm_profile_to_path("foot") == "foot"
        assert client._osrm_profile_to_path("bike") == "cycling"
        assert client._osrm_profile_to_path("car") == "driving"
        assert client._osrm_profile_to_path("unknown") == "foot"  # 기본값

