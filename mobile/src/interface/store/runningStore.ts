/**
 * Running Store (Zustand)
 * 러닝 세션 및 통계 상태 관리
 */

import { create } from 'zustand';
import { RunningSession } from '../../domain/entities/RunningSession';
import { Coordinate } from '../../domain/valueObjects/Coordinate';

interface RunningStore {
  // State
  session: RunningSession | null;
  isRunning: boolean;
  isPaused: boolean;
  currentLocation: Coordinate | null;
  stats: {
    distance: number;
    duration: number;
    pace: number;
    speed: number;
    elevationGain: number;
  };

  // Actions
  startRunning: (courseId?: string) => Promise<void>;
  pauseRunning: () => void;
  resumeRunning: () => void;
  updateLocation: (location: Coordinate) => void;
  finishRunning: () => Promise<RunningSession>;
  reset: () => void;
}

export const useRunningStore = create<RunningStore>((set, get) => ({
  session: null,
  isRunning: false,
  isPaused: false,
  currentLocation: null,
  stats: {
    distance: 0,
    duration: 0,
    pace: 0,
    speed: 0,
    elevationGain: 0,
  },

  startRunning: async (courseId) => {
    try {
      const { runningRepository } = await import('../../application/repositories/RunningRepository');
      const { currentLocation } = get();

      if (!currentLocation) {
        throw new Error('Current location is not available');
      }

      const response = await runningRepository.startRunning({
        course_id: courseId,
        start_location: {
          latitude: currentLocation.latitude,
          longitude: currentLocation.longitude,
        },
      });

      const session: RunningSession = {
        id: response.id,
        courseId,
        startTime: new Date(response.start_time),
        locations: [],
        totalDistance: 0,
        duration: 0,
        avgPace: 0,
        avgSpeed: 0,
        elevationGain: 0,
      };

      set({
        session,
        isRunning: true,
        isPaused: false,
        stats: {
          distance: 0,
          duration: 0,
          pace: 0,
          speed: 0,
          elevationGain: 0,
        },
      });
    } catch (error: any) {
      console.error('Failed to start running:', error);
      throw error;
    }
  },

  pauseRunning: () => {
    set({ isPaused: true, isRunning: false });
  },

  resumeRunning: () => {
    set({ isPaused: false, isRunning: true });
  },

  updateLocation: async (location) => {
    const state = get();
    if (!state.session) return;

    try {
      const { runningRepository } = await import('../../application/repositories/RunningRepository');

      // Send location update to backend
      await runningRepository.updateLocation(state.session.id, {
        location: {
          latitude: location.latitude,
          longitude: location.longitude,
          timestamp: new Date().toISOString(),
        },
      });

      const locations = [...state.session.locations, location];
      const distance = calculateTotalDistance(locations);
      const duration = Math.floor((Date.now() - state.session.startTime.getTime()) / 1000);
      const pace = distance > 0 ? (duration / 60) / distance : 0; // min/km
      const speed = distance > 0 ? (distance / duration) * 3600 : 0; // km/h

      const updatedSession: RunningSession = {
        ...state.session,
        locations,
        totalDistance: distance,
        duration,
        avgPace: pace,
        avgSpeed: speed,
      };

      set({
        session: updatedSession,
        currentLocation: location,
        stats: {
          distance,
          duration,
          pace,
          speed,
          elevationGain: state.stats.elevationGain, // TODO: 실제 고도 계산
        },
      });
    } catch (error: any) {
      console.error('Failed to update location:', error);
    }
  },

  finishRunning: async () => {
    const state = get();
    if (!state.session) {
      throw new Error('No active session');
    }

    try {
      const { runningRepository } = await import('../../application/repositories/RunningRepository');
      const { currentLocation } = state;

      if (!currentLocation) {
        throw new Error('Current location is not available');
      }

      await runningRepository.finishRunning(state.session.id, {
        end_location: {
          latitude: currentLocation.latitude,
          longitude: currentLocation.longitude,
        },
        route: state.session.locations.map(loc => ({
          lat: loc.latitude,
          lon: loc.longitude,
          timestamp: new Date().toISOString(),
        })),
      });

      const finishedSession: RunningSession = {
        ...state.session,
        endTime: new Date(),
      };

      set({
        session: finishedSession,
        isRunning: false,
        isPaused: false,
      });

      return finishedSession;
    } catch (error: any) {
      console.error('Failed to finish running:', error);
      throw error;
    }
  },

  reset: () => {
    set({
      session: null,
      isRunning: false,
      isPaused: false,
      currentLocation: null,
      stats: {
        distance: 0,
        duration: 0,
        pace: 0,
        speed: 0,
        elevationGain: 0,
      },
    });
  },
}));

/**
 * Haversine 공식을 사용한 거리 계산 (km)
 */
function calculateTotalDistance(coordinates: Coordinate[]): number {
  if (coordinates.length < 2) return 0;

  let totalDistance = 0;
  for (let i = 1; i < coordinates.length; i++) {
    totalDistance += haversineDistance(
      coordinates[i - 1],
      coordinates[i]
    );
  }
  return totalDistance;
}

/**
 * Haversine 공식: 두 좌표 간 거리 계산 (km)
 */
function haversineDistance(coord1: Coordinate, coord2: Coordinate): number {
  const R = 6371; // 지구 반지름 (km)
  const dLat = toRadians(coord2.latitude - coord1.latitude);
  const dLon = toRadians(coord2.longitude - coord1.longitude);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRadians(coord1.latitude)) *
    Math.cos(toRadians(coord2.latitude)) *
    Math.sin(dLon / 2) *
    Math.sin(dLon / 2);

  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function toRadians(degrees: number): number {
  return degrees * (Math.PI / 180);
}

