/**
 * RunningSession Entity
 * 러닝 세션 엔티티
 */

import { Coordinate } from '../valueObjects/Coordinate';

export interface RunningSession {
  id: string;
  courseId?: string;
  startTime: Date;
  endTime?: Date;
  locations: Coordinate[];
  totalDistance: number; // km
  duration: number; // seconds
  avgPace: number; // min/km
  avgSpeed: number; // km/h
  elevationGain: number; // m
}

