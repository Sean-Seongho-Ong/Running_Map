/**
 * Course Entity
 * 러닝 코스 엔티티
 */

import { Coordinate } from '../valueObjects/Coordinate';
import { Distance } from '../valueObjects/Distance';

export interface Course {
  id: string;
  name?: string;
  startPoint: Coordinate;
  polyline: Coordinate[];
  distance: Distance;
  elevationGain?: number;
  createdAt: Date;
  isPublic: boolean;
  userId?: string;
}

