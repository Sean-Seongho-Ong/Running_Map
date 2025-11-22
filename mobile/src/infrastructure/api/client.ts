import axios, { AxiosError, AxiosInstance, AxiosResponse } from 'axios';
import { config } from '../../config';
import { createLogger } from '../../utils/logger';

const logger = createLogger('API Client');

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
        logger.info(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        logger.error('API Request Error', error);
        return Promise.reject(error);
    }
);

// Response Interceptor
apiClient.interceptors.response.use(
    (response: AxiosResponse) => {
        logger.info(`API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error: AxiosError) => {
        if (error.response) {
            // 민감 정보는 로그에 기록하지 않음 (규칙 10)
            logger.error(
                `API Error: ${error.response.status} ${error.config?.url}`,
                { status: error.response.status, url: error.config?.url }
            );
        } else if (error.request) {
            logger.error('API Error: No response received', { request: 'Network error' });
        } else {
            logger.error('API Error: Request setup failed', { message: error.message });
        }
        return Promise.reject(error);
    }
);

export default apiClient;
