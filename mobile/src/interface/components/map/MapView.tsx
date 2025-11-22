/**
 * MapView 컴포넌트
 * react-native-maps 기반, OSM 타일 지원
 */

import React, { useRef, useEffect } from 'react';
import MapView, { PROVIDER_DEFAULT, Polyline, Marker, Region } from 'react-native-maps';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { Coordinate } from '../../../domain/valueObjects/Coordinate';

interface CustomMapViewProps {
  initialLocation: Coordinate;
  coursePolyline?: Coordinate[];
  currentLocation?: Coordinate;
  courseDistance?: number;
  onRegionChange?: (region: Region) => void;
  showLocationButton?: boolean;
  style?: object;
}

export const CustomMapView: React.FC<CustomMapViewProps> = ({
  initialLocation,
  coursePolyline,
  currentLocation,
  courseDistance,
  onRegionChange,
  showLocationButton = false,
  style,
}) => {
  const mapRef = useRef<MapView>(null);
  
  const initialRegion: Region = {
    latitude: initialLocation.latitude,
    longitude: initialLocation.longitude,
    latitudeDelta: 0.01,
    longitudeDelta: 0.01,
  };

  // 코스가 생성되면 자동으로 줌 조정
  useEffect(() => {
    if (coursePolyline && coursePolyline.length > 0 && mapRef.current) {
      const coordinates = coursePolyline.map(coord => ({
        latitude: coord.latitude,
        longitude: coord.longitude,
      }));

      // 모든 좌표를 포함하는 영역 계산
      const minLat = Math.min(...coordinates.map(c => c.latitude));
      const maxLat = Math.max(...coordinates.map(c => c.latitude));
      const minLon = Math.min(...coordinates.map(c => c.longitude));
      const maxLon = Math.max(...coordinates.map(c => c.longitude));

      const latDelta = (maxLat - minLat) * 1.5; // 여유 공간 추가
      const lonDelta = (maxLon - minLon) * 1.5;

      mapRef.current.fitToCoordinates(coordinates, {
        edgePadding: { top: 50, right: 50, bottom: 50, left: 50 },
        animated: true,
      });
    }
  }, [coursePolyline]);
  
  const startPoint = coursePolyline && coursePolyline.length > 0 
    ? coursePolyline[0] 
    : null;
  const endPoint = coursePolyline && coursePolyline.length > 0 
    ? coursePolyline[coursePolyline.length - 1] 
    : null;
  
  return (
    <View style={[styles.container, style]}>
      <MapView
        ref={mapRef}
        provider={PROVIDER_DEFAULT}
        style={styles.map}
        initialRegion={initialRegion}
        customMapStyle={[]} // OSM 타일 사용 시 빈 배열
        onRegionChangeComplete={onRegionChange}
        showsUserLocation={false} // 커스텀 마커 사용
        showsMyLocationButton={false}
      >
        {/* 현재 위치 마커 */}
        {currentLocation && (
          <Marker
            coordinate={{
              latitude: currentLocation.latitude,
              longitude: currentLocation.longitude,
            }}
            title="현재 위치"
            pinColor="#FF6B35"
          />
        )}
        
        {/* 코스 시작점 마커 */}
        {startPoint && (
          <Marker
            coordinate={{
              latitude: startPoint.latitude,
              longitude: startPoint.longitude,
            }}
            title="시작점"
            pinColor="#4CAF50"
          />
        )}

        {/* 코스 끝점 마커 */}
        {endPoint && startPoint && 
         (endPoint.latitude !== startPoint.latitude || 
          endPoint.longitude !== startPoint.longitude) && (
          <Marker
            coordinate={{
              latitude: endPoint.latitude,
              longitude: endPoint.longitude,
            }}
            title="끝점"
            pinColor="#F44336"
          />
        )}
        
        {/* 코스 폴리라인 */}
        {coursePolyline && coursePolyline.length > 0 && (
          <Polyline
            coordinates={coursePolyline.map(coord => ({
              latitude: coord.latitude,
              longitude: coord.longitude,
            }))}
            strokeColor="#FF6B35"
            strokeWidth={4}
          />
        )}
      </MapView>
      
      {/* 거리 정보 오버레이 */}
      {courseDistance !== undefined && courseDistance > 0 && (
        <View style={styles.distanceOverlay}>
          <Text style={styles.distanceText}>
            {courseDistance.toFixed(2)} km
          </Text>
        </View>
      )}

      {/* 현재 위치로 이동 버튼 */}
      {showLocationButton && currentLocation && (
        <TouchableOpacity
          style={styles.locationButton}
          onPress={() => {
            mapRef.current?.animateToRegion({
              latitude: currentLocation.latitude,
              longitude: currentLocation.longitude,
              latitudeDelta: 0.01,
              longitudeDelta: 0.01,
            }, 500);
          }}
        >
          <Text style={styles.locationButtonText}>📍</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    position: 'relative',
  },
  map: {
    flex: 1,
  },
  distanceOverlay: {
    position: 'absolute',
    top: 16,
    right: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  distanceText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  locationButton: {
    position: 'absolute',
    bottom: 16,
    right: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  locationButtonText: {
    fontSize: 24,
  },
});

