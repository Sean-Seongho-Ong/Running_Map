/**
 * Location Store (Zustand)
 * 현재 위치 관리
 */

import { create } from 'zustand';
import { Coordinate } from '../../domain/valueObjects/Coordinate';

interface LocationStore {
  // State
  currentLocation: Coordinate | null;
  isLocationEnabled: boolean;
  locationError: string | null;
  
  // Actions
  setCurrentLocation: (location: Coordinate) => void;
  setLocationEnabled: (enabled: boolean) => void;
  setLocationError: (error: string | null) => void;
  clearLocation: () => void;
}

export const useLocationStore = create<LocationStore>((set) => ({
  currentLocation: null,
  isLocationEnabled: false,
  locationError: null,
  
  setCurrentLocation: (location) => {
    set({ currentLocation: location, locationError: null });
  },
  
  setLocationEnabled: (enabled) => {
    set({ isLocationEnabled: enabled });
  },
  
  setLocationError: (error) => {
    set({ locationError: error });
  },
  
  clearLocation: () => {
    set({
      currentLocation: null,
      locationError: null,
    });
  },
}));

