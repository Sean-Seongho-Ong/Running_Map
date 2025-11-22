/**
 * RunningScreen
 * 러닝 추적 화면
 */

import React from 'react';
import { View, StyleSheet } from 'react-native';
import { CustomMapView } from '../components/map/MapView';
import { RunningStats } from '../components/running/RunningStats';
import { Button } from '../components/common/Button';
import { useTheme } from '../hooks/useTheme';
import { useLocationStore } from '../store/locationStore';
import { useRunningStore } from '../store/runningStore';
import { Theme } from '../../theme';

export const RunningScreen: React.FC = () => {
  const theme = useTheme();
  const styles = createStyles(theme);
  const { currentLocation } = useLocationStore();
  const {
    isRunning,
    isPaused,
    stats,
    pauseRunning,
    resumeRunning,
    finishRunning,
  } = useRunningStore();
  
  const handlePause = () => {
    if (isPaused) {
      resumeRunning();
    } else {
      pauseRunning();
    }
  };
  
  const handleFinish = async () => {
    await finishRunning();
    // TODO: 결과 화면으로 이동
  };
  
  if (!currentLocation) {
    return null; // TODO: 로딩 화면
  }
  
  return (
    <View style={styles.container}>
      <View style={styles.statsContainer}>
        <RunningStats
          distance={stats.distance}
          duration={stats.duration}
          pace={stats.pace}
          speed={stats.speed}
          elevationGain={stats.elevationGain}
        />
      </View>
      <CustomMapView
        initialLocation={currentLocation}
        currentLocation={currentLocation}
        style={styles.map}
      />
      <View style={styles.controlContainer}>
        <Button
          title={isPaused ? '재개' : '일시정지'}
          onPress={handlePause}
          variant="outline"
          style={styles.controlButton}
        />
        <Button
          title="종료"
          onPress={handleFinish}
          variant="primary"
          style={styles.controlButton}
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
    statsContainer: {
      padding: theme.spacing.md,
      backgroundColor: theme.colors.surface,
    },
    map: {
      flex: 1,
    },
    controlContainer: {
      flexDirection: 'row',
      padding: theme.spacing.md,
      backgroundColor: theme.colors.surface,
      gap: theme.spacing.sm,
    },
    controlButton: {
      flex: 1,
    },
  });

