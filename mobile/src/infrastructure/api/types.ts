import { Course } from '../../domain/entities/Course';
import { RunningSession } from '../../domain/entities/RunningSession';

export interface ApiResponse<T> {
    status: string;
    data?: T;
    error?: {
        code: string;
        message: string;
        details?: any;
    };
}

export interface CourseGenerationRequest {
    start_point: {
        latitude: number;
        longitude: number;
    };
    target_distance: number;
}

export interface CourseGenerationResult {
    id: string;
    polyline: { lat: number; lon: number }[];
    distance: number;
    relative_error: number;
    algorithm: string;
    iterations: number;
    step_used?: number;
    metadata?: any;
}

export interface CourseGenerationResponse {
    status: string;
    course?: CourseGenerationResult;
    error?: {
        code: string;
        message: string;
        details?: any;
    };
}

export interface CourseListItem {
    id: string;
    name: string;
    distance: number;
    is_public: boolean;
    created_at: string;
}

export interface CourseListResponse {
    courses: CourseListItem[];
    total: number;
    limit: number;
    offset: number;
}

export interface CourseSaveRequest {
    name: string;
    polyline: { lat: number; lon: number }[];
    distance: number;
    is_public: boolean;
}

export interface CourseSaveResponse {
    id: string;
    name: string;
    created_at: string;
}

export interface CourseResponse {
    id: string;
    name: string;
    distance: number;
    polyline: { lat: number; lon: number }[];
    is_public: boolean;
    metadata?: any;
    created_at: string;
}

export interface RunningStartRequest {
    course_id?: string;
    start_location: {
        latitude: number;
        longitude: number;
    };
}

export interface RunningLocationUpdateRequest {
    location: {
        latitude: number;
        longitude: number;
        altitude?: number;
        timestamp: string;
    };
    timestamp: string;
}

export interface RunningFinishRequest {
    end_location: {
        latitude: number;
        longitude: number;
    };
}

export interface RunningSessionStartResponse {
    session_id: string;
    started_at: string;
}

export interface RunningSessionResponse {
    id: string;
    start_time: string;
    end_time?: string;
    total_distance: number;
    total_duration?: number;
    avg_pace?: number;
    elevation_gain?: number;
    route_polyline?: { lat: number; lon: number }[];
}
