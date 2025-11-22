/**
 * RunningStats 컴포넌트
 * 러닝 통계 표시 (거리, 시간, 페이스, 속도, 고저차)
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface RunningStatsProps {
  distance: number;      // km
  duration: number;      // 초
  pace: number;         // 분/km
  speed: number;        // km/h
  elevationGain: number; // m
}

export const RunningStats: React.FC<RunningStatsProps> = ({
  distance,
  duration,
  pace,
  speed,
  elevationGain,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme);
  
  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  
  const formatPace = (paceMinPerKm: number): string => {
    const minutes = Math.floor(paceMinPerKm);
    const seconds = Math.floor((paceMinPerKm - minutes) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{distance.toFixed(2)}</Text>
          <Text style={styles.statLabel}>거리 (km)</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{formatTime(duration)}</Text>
          <Text style={styles.statLabel}>시간</Text>
        </View>
      </View>
      
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{formatPace(pace)}</Text>
          <Text style={styles.statLabel}>페이스 (분/km)</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{speed.toFixed(1)}</Text>
          <Text style={styles.statLabel}>속도 (km/h)</Text>
        </View>
      </View>
      
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>+{elevationGain.toFixed(0)}</Text>
          <Text style={styles.statLabel}>고저차 (m)</Text>
        </View>
      </View>
    </View>
  );
};

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      backgroundColor: theme.colors.surface,
      padding: theme.spacing.md,
      borderRadius: 12,
    },
    row: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      marginBottom: theme.spacing.md,
    },
    statItem: {
      alignItems: 'center',
      flex: 1,
    },
    statValue: {
      ...theme.typography.statMedium,
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    statLabel: {
      ...theme.typography.caption,
      color: theme.colors.textSecondary,
    },
  });

