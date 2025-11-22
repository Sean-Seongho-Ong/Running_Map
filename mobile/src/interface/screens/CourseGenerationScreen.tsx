/**
 * CourseGenerationScreen
 * 코스 생성 화면
 */

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { CustomMapView } from '../components/map/MapView';
import { Input } from '../components/common/Input';
import { Button } from '../components/common/Button';
import { Loading } from '../components/common/Loading';
import { CourseDetailInfo } from '../components/course/CourseDetailInfo';
import { useTheme } from '../hooks/useTheme';
import { useLocationStore } from '../store/locationStore';
import { useCourseStore } from '../store/courseStore';
import { Distance } from '../../domain/valueObjects/Distance';
import { Theme } from '../../theme';

export const CourseGenerationScreen: React.FC = () => {
  const theme = useTheme();
  const styles = createStyles(theme);
  const navigation = useNavigation();
  const { currentLocation } = useLocationStore();
  const { 
    generateCourse, 
    isGenerating, 
    generationError, 
    generatedCourse,
    generationMetadata,
    clearGeneratedCourse,
  } = useCourseStore();

  const [distance, setDistance] = useState('');
  const [lastTargetDistance, setLastTargetDistance] = useState<number | null>(null);

  // 코스 생성 성공 시 알림 (선택적 - 상세 정보가 표시되므로 자동 이동 제거)
  useEffect(() => {
    if (generatedCourse && !isGenerating && generationMetadata) {
      // 상세 정보가 표시되므로 자동으로 화면 이동하지 않음
      // 사용자가 직접 확인 후 이동할 수 있도록 함
    }
  }, [generatedCourse, isGenerating, generationMetadata]);

  // 에러 발생 시 알림 (상세 정보 표시 및 재시도 옵션)
  useEffect(() => {
    if (generationError && !isGenerating) {
      Alert.alert(
        '코스 생성 실패',
        generationError,
        [
          {
            text: '다시 시도',
            onPress: () => {
              if (lastTargetDistance) {
                handleRegenerate();
              }
            },
            style: 'default',
          },
          {
            text: '확인',
            style: 'cancel',
          },
        ]
      );
    }
  }, [generationError, isGenerating, lastTargetDistance]);

  const handleGenerate = async () => {
    if (!currentLocation || !distance) return;

    const targetDistance = parseFloat(distance);
    setLastTargetDistance(targetDistance);
    await generateCourse(currentLocation, new Distance(targetDistance));
  };

  const handleRegenerate = async () => {
    if (!currentLocation || !lastTargetDistance) return;
    clearGeneratedCourse();
    await generateCourse(currentLocation, new Distance(lastTargetDistance));
  };

  const handleUseCourse = async () => {
    if (generatedCourse) {
      // 코스를 선택된 코스로 설정하고 MapScreen으로 이동
      // generatedCourse는 이미 store에 있으므로 MapScreen에서 자동으로 표시됨
      navigation.navigate('MapTab' as never);
    } else {
      navigation.goBack();
    }
  };

  const handlePreset = (presetDistance: string) => {
    setDistance(presetDistance);
  };

  if (!currentLocation) {
    return <Loading message="위치 정보를 가져오는 중..." />;
  }

  return (
    <View style={styles.container}>
      <CustomMapView
        initialLocation={currentLocation}
        coursePolyline={generatedCourse?.polyline}
        currentLocation={currentLocation}
        courseDistance={generatedCourse?.distance.kilometers}
        style={styles.map}
      />
      <View style={styles.inputContainer}>
        <ScrollView>
          {generatedCourse && generationMetadata ? (
            <>
              <CourseDetailInfo
                targetDistance={generationMetadata.targetDistance || 0}
                actualDistance={generatedCourse.distance.kilometers}
                relativeError={generationMetadata.relativeError || 0}
                algorithm={generationMetadata.algorithm || ''}
                iterations={generationMetadata.iterations || 0}
                stepUsed={generationMetadata.stepUsed}
                status={generationMetadata.status}
              />
              <View style={styles.buttonGroup}>
                <Button
                  title="이 코스 사용"
                  onPress={handleUseCourse}
                  variant="primary"
                  fullWidth
                  style={styles.button}
                />
                <Button
                  title="다시 생성"
                  onPress={handleRegenerate}
                  variant="outline"
                  fullWidth
                  style={styles.button}
                  disabled={isGenerating}
                />
              </View>
            </>
          ) : (
            <>
              <Input
                label="목표 거리 (km)"
                value={distance}
                onChangeText={setDistance}
                keyboardType="decimal-pad"
                placeholder="예: 5.0"
                error={generationError || undefined}
              />
              <View style={styles.presetContainer}>
                <Button
                  title="3km"
                  onPress={() => handlePreset('3')}
                  variant="outline"
                  size="small"
                  style={styles.presetButton}
                />
                <Button
                  title="5km"
                  onPress={() => handlePreset('5')}
                  variant="outline"
                  size="small"
                  style={styles.presetButton}
                />
                <Button
                  title="10km"
                  onPress={() => handlePreset('10')}
                  variant="outline"
                  size="small"
                  style={styles.presetButton}
                />
              </View>
              {isGenerating ? (
                <Loading message="코스를 생성하는 중..." />
              ) : (
                <Button
                  title="코스 생성"
                  onPress={handleGenerate}
                  variant="primary"
                  disabled={!distance}
                  fullWidth
                />
              )}
            </>
          )}
        </ScrollView>
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
    map: {
      flex: 0.6,
    },
    inputContainer: {
      flex: 0.4,
      backgroundColor: theme.colors.surface,
      padding: theme.spacing.md,
    },
    presetContainer: {
      flexDirection: 'row',
      gap: theme.spacing.sm,
      marginBottom: theme.spacing.md,
    },
    presetButton: {
      flex: 1,
    },
    buttonGroup: {
      marginTop: theme.spacing.md,
      gap: theme.spacing.sm,
    },
    button: {
      marginBottom: theme.spacing.sm,
    },
  });

