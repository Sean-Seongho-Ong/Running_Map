/**
 * CoursePolyline 컴포넌트
 * 코스 경로를 폴리라인으로 표시
 */

import React from 'react';
import { Polyline } from 'react-native-maps';
import { Coordinate } from '../../../domain/valueObjects/Coordinate';

interface CoursePolylineProps {
  coordinates: Coordinate[];
  color?: string;
  strokeWidth?: number;
}

export const CoursePolyline: React.FC<CoursePolylineProps> = ({
  coordinates,
  color = '#FF6B35',
  strokeWidth = 4,
}) => {
  if (!coordinates || coordinates.length === 0) {
    return null;
  }
  
  return (
    <Polyline
      coordinates={coordinates.map(coord => ({
        latitude: coord.latitude,
        longitude: coord.longitude,
      }))}
      strokeColor={color}
      strokeWidth={strokeWidth}
    />
  );
};

