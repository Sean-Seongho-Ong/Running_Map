/**
 * MapScreen
 * 지도 메인 화면
 */

import React, { useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { CustomMapView } from '../components/map/MapView';
import { Button } from '../components/common/Button';
import { useTheme } from '../hooks/useTheme';
import { useLocationStore } from '../store/locationStore';
import { useCourseStore } from '../store/courseStore';
import { Coordinate } from '../../domain/valueObjects/Coordinate';
import { Theme } from '../../theme';

export const MapScreen: React.FC = () => {
  const theme = useTheme();
  const styles = createStyles(theme);
  const navigation = useNavigation();
  const { currentLocation, setCurrentLocation } = useLocationStore();
  const { generatedCourse } = useCourseStore();

  // 초기 위치 설정 (임시)
  useEffect(() => {
    if (!currentLocation) {
      // TODO: 실제 GPS 위치 가져오기
      setCurrentLocation(new Coordinate(37.5665, 126.9780)); // 서울시청
    }
  }, []);

  const handleGenerateCourse = () => {
    navigation.navigate('CourseGeneration' as never);
  };

  const handleViewCourses = () => {
    navigation.navigate('CoursesTab' as never);
  };

  if (!currentLocation) {
    return null; // TODO: 로딩 화면
  }

  return (
    <View style={styles.container}>
      <View style={styles.mapContainer}>
        <CustomMapView
          initialLocation={currentLocation}
          coursePolyline={generatedCourse?.polyline}
          currentLocation={currentLocation}
          courseDistance={generatedCourse?.distance.kilometers}
          showLocationButton={true}
          style={styles.map}
        />
      </View>
      <View style={styles.buttonContainer}>
        <Button
          title="코스 생성"
          onPress={handleGenerateCourse}
          variant="primary"
          fullWidth
          style={styles.button}
        />
        <Button
          title="내 코스"
          onPress={handleViewCourses}
          variant="outline"
          fullWidth
          style={styles.button}
        />
      </View>
    </View>
  );
};

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: theme.colors.background,
    },
    mapContainer: {
      flex: 1,
      marginTop: 10, // Figma 디자인: 상단 여백 10px
      marginHorizontal: 10, // Figma 디자인: 좌우 여백 10px
      backgroundColor: theme.colors.mapBackground, // Figma 디자인: #d9d9d9
      borderRadius: 0, // 필요시 조정
    },
    map: {
      flex: 1,
    },
    buttonContainer: {
      padding: theme.spacing.md, // Figma 디자인: 16px 패딩
      backgroundColor: theme.colors.surface, // Figma 디자인: 흰색
      gap: theme.spacing.sm, // 버튼 간격
    },
    button: {
      marginBottom: 0, // gap으로 간격 관리
    },
  });

