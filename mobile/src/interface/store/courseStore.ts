/**
 * Course Store (Zustand)
 * 코스 생성, 저장, 로드 상태 관리
 */

import { create } from 'zustand';
import { Course } from '../../domain/entities/Course';
import { Coordinate } from '../../domain/valueObjects/Coordinate';
import { Distance } from '../../domain/valueObjects/Distance';

interface CourseGenerationMetadata {
  status: string;
  relativeError?: number;
  algorithm?: string;
  iterations?: number;
  stepUsed?: number;
  targetDistance?: number;
}

interface CourseStore {
  // State
  courses: Course[];
  selectedCourse: Course | null;
  generatedCourse: Course | null;
  generationMetadata: CourseGenerationMetadata | null;
  isGenerating: boolean;
  generationError: string | null;

  // Actions
  generateCourse: (
    startPoint: Coordinate,
    targetDistance: Distance,
    parameters?: any
  ) => Promise<void>;
  selectCourse: (courseId: string) => void;
  saveCourse: (course: Course, name: string) => Promise<void>;
  loadCourses: () => Promise<void>;
  clearGeneratedCourse: () => void;
}

export const useCourseStore = create<CourseStore>((set, get) => ({
  courses: [],
  selectedCourse: null,
  generatedCourse: null,
  generationMetadata: null,
  isGenerating: false,
  generationError: null,

  generateCourse: async (startPoint, targetDistance, parameters) => {
    set({ isGenerating: true, generationError: null, generationMetadata: null });
    try {
      const { courseRepository } = await import('../../application/repositories/CourseRepository');

      const response = await courseRepository.generateCourse({
        start_point: {
          latitude: startPoint.latitude,
          longitude: startPoint.longitude,
        },
        target_distance: targetDistance.kilometers,
      });

      if (!response.course) {
        throw new Error('코스 생성 결과가 없습니다.');
      }

      const course: Course = {
        id: response.course.id,
        name: '',
        startPoint,
        polyline: response.course.polyline.map(p => new Coordinate(p.lat, p.lon)),
        distance: new Distance(response.course.distance),
        createdAt: new Date(),
        isPublic: false,
      };

      const metadata: CourseGenerationMetadata = {
        status: response.status,
        relativeError: response.course.relative_error,
        algorithm: response.course.algorithm,
        iterations: response.course.iterations,
        stepUsed: response.course.step_used,
        targetDistance: targetDistance.kilometers,
      };

      set({ 
        generatedCourse: course, 
        generationMetadata: metadata,
        isGenerating: false 
      });
    } catch (error: any) {
      set({
        generationError: error.message || '코스 생성에 실패했습니다.',
        isGenerating: false,
      });
    }
  },

  selectCourse: (courseId) => {
    const course = get().courses.find(c => c.id === courseId);
    set({ selectedCourse: course || null });
  },

  saveCourse: async (course, name) => {
    try {
      const { courseRepository } = await import('../../application/repositories/CourseRepository');

      const response = await courseRepository.saveCourse({
        id: course.id,
        name,
        distance: course.distance.kilometers,
        polyline: course.polyline.map(c => ({ lat: c.latitude, lon: c.longitude })),
        is_public: course.isPublic || false,
        created_at: course.createdAt.toISOString(),
      });

      // 저장 후 상세 정보를 다시 조회하여 전체 정보 가져오기
      const savedCourseDetail = await courseRepository.getCourse(response.id);

      const savedCourse: Course = {
        id: savedCourseDetail.id,
        name: savedCourseDetail.name,
        startPoint: new Coordinate(savedCourseDetail.polyline[0].lat, savedCourseDetail.polyline[0].lon),
        polyline: savedCourseDetail.polyline.map(p => new Coordinate(p.lat, p.lon)),
        distance: new Distance(savedCourseDetail.distance),
        createdAt: new Date(savedCourseDetail.created_at),
        isPublic: savedCourseDetail.is_public,
      };

      set(state => ({
        courses: [...state.courses, savedCourse],
      }));
    } catch (error: any) {
      throw new Error(error.message || '코스 저장에 실패했습니다.');
    }
  },

  loadCourses: async () => {
    try {
      const { courseRepository } = await import('../../application/repositories/CourseRepository');

      const response = await courseRepository.listCourses();

      const courses: Course[] = response.map(c => ({
        id: c.id,
        name: c.name,
        startPoint: new Coordinate(c.polyline[0].lat, c.polyline[0].lon),
        polyline: c.polyline.map(p => new Coordinate(p.lat, p.lon)),
        distance: new Distance(c.distance),
        createdAt: new Date(c.created_at),
        isPublic: c.is_public,
      }));

      set({ courses });
    } catch (error: any) {
      console.error('Failed to load courses:', error);
    }
  },

  clearGeneratedCourse: () => {
    set({ generatedCourse: null, generationMetadata: null });
  },
}));

