import apiClient from '../../infrastructure/api/client';
import { API_ENDPOINTS } from '../../infrastructure/api/endpoints';
import {
    ApiResponse,
    CourseGenerationRequest,
    CourseGenerationResponse,
    CourseResponse,
    CourseListResponse,
    CourseSaveRequest,
    CourseSaveResponse,
} from '../../infrastructure/api/types';

export class CourseRepository {
    async generateCourse(
        request: CourseGenerationRequest
    ): Promise<CourseGenerationResponse> {
        const response = await apiClient.post<CourseGenerationResponse>(
            API_ENDPOINTS.COURSES.GENERATE,
            request
        );

        if (response.data.status === 'OK' || response.data.status === 'BEST_EFFORT') {
            return response.data;
        }
        throw new Error(response.data.error?.message || 'Failed to generate course');
    }

    async saveCourse(course: CourseResponse): Promise<CourseSaveResponse> {
        // CourseSaveRequestDTO 형식으로 변환
        const saveRequest: CourseSaveRequest = {
            name: course.name,
            polyline: course.polyline,
            distance: course.distance,
            is_public: course.is_public,
        };

        const response = await apiClient.post<CourseSaveResponse>(
            API_ENDPOINTS.COURSES.BASE,
            saveRequest
        );

        return response.data;
    }

    async listCourses(): Promise<CourseResponse[]> {
        const response = await apiClient.get<CourseListResponse>(
            API_ENDPOINTS.COURSES.BASE
        );

        // CourseListResponse를 CourseResponse[]로 변환
        // 목록 조회는 polyline이 없으므로, 상세 조회가 필요할 때 다시 조회해야 함
        return response.data.courses.map(course => ({
            id: course.id,
            name: course.name,
            distance: course.distance,
            polyline: [], // 목록 조회에서는 polyline이 없음
            is_public: course.is_public,
            created_at: course.created_at,
        }));
    }

    async getCourse(id: string): Promise<CourseResponse> {
        const response = await apiClient.get<CourseResponse>(
            API_ENDPOINTS.COURSES.DETAIL(id)
        );

        return response.data;
    }
}

export const courseRepository = new CourseRepository();
