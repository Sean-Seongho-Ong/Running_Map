import apiClient from '../../infrastructure/api/client';
import { API_ENDPOINTS } from '../../infrastructure/api/endpoints';
import {
    ApiResponse,
    RunningFinishRequest,
    RunningLocationUpdateRequest,
    RunningSessionResponse,
    RunningStartRequest,
} from '../../infrastructure/api/types';

export class RunningRepository {
    async startRunning(
        request: RunningStartRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<ApiResponse<RunningSessionResponse>>(
            API_ENDPOINTS.RUNNING.START,
            request
        );

        if (response.data.status === 'success' && response.data.data) {
            return response.data.data;
        }
        throw new Error(response.data.error?.message || 'Failed to start running');
    }

    async updateLocation(
        sessionId: string,
        request: RunningLocationUpdateRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<ApiResponse<RunningSessionResponse>>(
            API_ENDPOINTS.RUNNING.LOCATION(sessionId),
            request
        );

        if (response.data.status === 'success' && response.data.data) {
            return response.data.data;
        }
        throw new Error(response.data.error?.message || 'Failed to update location');
    }

    async finishRunning(
        sessionId: string,
        request: RunningFinishRequest
    ): Promise<RunningSessionResponse> {
        const response = await apiClient.post<ApiResponse<RunningSessionResponse>>(
            API_ENDPOINTS.RUNNING.FINISH(sessionId),
            request
        );

        if (response.data.status === 'success' && response.data.data) {
            return response.data.data;
        }
        throw new Error(response.data.error?.message || 'Failed to finish running');
    }
}

export const runningRepository = new RunningRepository();
