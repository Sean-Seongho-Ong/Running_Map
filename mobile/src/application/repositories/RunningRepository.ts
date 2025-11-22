import apiClient from '../../infrastructure/api/client';
import { API_ENDPOINTS } from '../../infrastructure/api/endpoints';
import {
    RunningFinishRequest,
    RunningLocationUpdateRequest,
    RunningSessionResponse,
    RunningSessionStartResponse,
    RunningStartRequest,
} from '../../infrastructure/api/types';

export class RunningRepository {
    async startRunning(
        request: RunningStartRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<RunningSessionStartResponse>(
            API_ENDPOINTS.RUNNING.START,
            request
        );

        // 백엔드 응답을 프론트엔드 형식으로 변환
        return {
            id: response.data.session_id,
            start_time: response.data.started_at,
            end_time: undefined,
            total_distance: 0,
            total_duration: undefined,
            avg_pace: undefined,
            elevation_gain: undefined,
            route_polyline: undefined,
        };
    }

    async updateLocation(
        sessionId: string,
        request: RunningLocationUpdateRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<{ session_id: string; stats: any; route_length: number }>(
            API_ENDPOINTS.RUNNING.LOCATION(sessionId),
            request
        );

        // 백엔드 응답을 프론트엔드 형식으로 변환
        return {
            id: response.data.session_id,
            start_time: '', // Location Update 응답에는 start_time이 없음
            end_time: undefined,
            total_distance: response.data.stats.distance || 0,
            total_duration: response.data.stats.duration || 0,
            avg_pace: response.data.stats.pace || 0,
            elevation_gain: response.data.stats.elevation_gain || 0,
            route_polyline: undefined,
        };
    }

    async finishRunning(
        sessionId: string,
        request: RunningFinishRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<{ session_id: string; stats: any; started_at: string; finished_at: string; route: { latitude: number; longitude: number }[] }>(
            API_ENDPOINTS.RUNNING.FINISH(sessionId),
            request
        );

        // 백엔드 응답을 프론트엔드 형식으로 변환
        return {
            id: response.data.session_id,
            start_time: response.data.started_at,
            end_time: response.data.finished_at,
            total_distance: response.data.stats.distance || 0,
            total_duration: response.data.stats.duration || 0,
            avg_pace: response.data.stats.pace || 0,
            elevation_gain: response.data.stats.elevation_gain || 0,
            route_polyline: response.data.route.map(coord => ({ lat: coord.latitude, lon: coord.longitude })),
        };
    }
}

export const runningRepository = new RunningRepository();
