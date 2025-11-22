/**
 * CourseDetailInfo
 * 코스 생성 결과 상세 정보 표시 컴포넌트
 */

import React from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { Card } from '../common/Card';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface CourseDetailInfoProps {
  targetDistance: number;
  actualDistance: number;
  relativeError: number;
  algorithm: string;
  iterations: number;
  stepUsed?: number;
  status: string;
}

export const CourseDetailInfo: React.FC<CourseDetailInfoProps> = ({
  targetDistance,
  actualDistance,
  relativeError,
  algorithm,
  iterations,
  stepUsed,
  status,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme);

  const getStatusColor = () => {
    switch (status) {
      case 'OK':
        return theme.colors.success;
      case 'BEST_EFFORT':
        return theme.colors.warning;
      case 'FAIL':
        return theme.colors.error;
      default:
        return theme.colors.text;
    }
  };

  const getStatusText = () => {
    switch (status) {
      case 'OK':
        return '완벽한 코스';
      case 'BEST_EFFORT':
        return '최선의 결과';
      case 'FAIL':
        return '생성 실패';
      default:
        return status;
    }
  };

  const getAlgorithmText = () => {
    switch (algorithm) {
      case 'STEP_ADAPTIVE':
        return 'Step 기반 적응형';
      case 'SP_BASED':
        return 'S-P 기반';
      case 'FALLBACK':
        return 'Fallback';
      default:
        return algorithm;
    }
  };

  const errorPercent = (relativeError * 100).toFixed(2);
  const distanceDiff = (actualDistance - targetDistance).toFixed(2);

  return (
    <Card style={styles.container} elevated>
      <View style={styles.header}>
        <Text style={styles.title}>코스 생성 결과</Text>
        <View style={[styles.statusBadge, { backgroundColor: getStatusColor() }]}>
          <Text style={styles.statusText}>{getStatusText()}</Text>
        </View>
      </View>

      <View style={styles.section}>
        <View style={styles.row}>
          <Text style={styles.label}>목표 거리:</Text>
          <Text style={styles.value}>{targetDistance.toFixed(2)} km</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>실제 거리:</Text>
          <Text style={styles.value}>{actualDistance.toFixed(2)} km</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>차이:</Text>
          <Text style={[styles.value, distanceDiff.startsWith('-') ? styles.negative : styles.positive]}>
            {distanceDiff.startsWith('-') ? '' : '+'}{distanceDiff} km
          </Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>상대 오차:</Text>
          <Text style={[styles.value, Math.abs(relativeError) < 0.1 ? styles.positive : styles.warning]}>
            {errorPercent}%
          </Text>
        </View>
      </View>

      <View style={styles.section}>
        <View style={styles.row}>
          <Text style={styles.label}>알고리즘:</Text>
          <Text style={styles.value}>{getAlgorithmText()}</Text>
        </View>
        <View style={styles.row}>
          <Text style={styles.label}>반복 횟수:</Text>
          <Text style={styles.value}>{iterations}회</Text>
        </View>
        {stepUsed !== undefined && (
          <View style={styles.row}>
            <Text style={styles.label}>Step 값:</Text>
            <Text style={styles.value}>{stepUsed.toFixed(2)} km</Text>
          </View>
        )}
      </View>
    </Card>
  );
};

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      padding: theme.spacing.md,
      marginVertical: theme.spacing.sm,
    },
    header: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: theme.spacing.md,
    },
    title: {
      fontSize: theme.typography.h2.fontSize,
      fontWeight: theme.typography.h2.fontWeight,
      color: theme.colors.text,
    },
    statusBadge: {
      paddingHorizontal: theme.spacing.sm,
      paddingVertical: theme.spacing.xs,
      borderRadius: theme.spacing.xs,
    },
    statusText: {
      fontSize: theme.typography.caption.fontSize,
      fontWeight: theme.typography.captionBold.fontWeight,
      color: theme.colors.surface,
    },
    section: {
      marginBottom: theme.spacing.md,
    },
    row: {
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      paddingVertical: theme.spacing.xs,
    },
    label: {
      fontSize: theme.typography.body.fontSize,
      color: theme.colors.textSecondary,
    },
    value: {
      fontSize: theme.typography.body.fontSize,
      fontWeight: theme.typography.bodyBold.fontWeight,
      color: theme.colors.text,
    },
    positive: {
      color: theme.colors.success,
    },
    negative: {
      color: theme.colors.error,
    },
    warning: {
      color: theme.colors.warning,
    },
  });

