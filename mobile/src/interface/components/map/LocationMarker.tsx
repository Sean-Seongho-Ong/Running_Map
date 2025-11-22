/**
 * LocationMarker 컴포넌트
 * 현재 위치 마커 표시
 */

import React from 'react';
import { Marker } from 'react-native-maps';
import { Coordinate } from '../../../domain/valueObjects/Coordinate';

interface LocationMarkerProps {
  coordinate: Coordinate;
  title?: string;
  color?: string;
}

export const LocationMarker: React.FC<LocationMarkerProps> = ({
  coordinate,
  title = '현재 위치',
  color = '#FF6B35',
}) => {
  return (
    <Marker
      coordinate={{
        latitude: coordinate.latitude,
        longitude: coordinate.longitude,
      }}
      title={title}
      pinColor={color}
    />
  );
};

