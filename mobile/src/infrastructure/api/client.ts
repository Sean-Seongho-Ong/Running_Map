import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios';
import { config } from '../../config';

const apiClient: AxiosInstance = axios.create({
    baseURL: config.API_BASE_URL,
    timeout: config.TIMEOUT,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor
apiClient.interceptors.request.use(
    (config) => {
        console.log(`[API Request] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('[API Request Error]', error);
        return Promise.reject(error);
    }
);

// Response Interceptor
apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        console.log(`[API Response] ${response.status} ${response.config.url}`);
        return response;
    },
    (error: AxiosError) => {
        if (error.response) {
            console.error(
                `[API Error] ${error.response.status} ${error.config?.url}`,
                error.response.data
            );
        } else if (error.request) {
            console.error('[API Error] No response received', error.request);
        } else {
            console.error('[API Error] Request setup failed', error.message);
        }
        return Promise.reject(error);
    }
);

export default apiClient;
