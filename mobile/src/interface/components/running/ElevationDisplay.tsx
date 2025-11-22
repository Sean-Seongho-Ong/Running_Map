/**
 * ElevationDisplay 컴포넌트
 * 고저차 전용 표시 컴포넌트
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface ElevationDisplayProps {
  elevationGain: number; // m
  elevationLoss?: number; // m
  currentElevation?: number; // m
  size?: 'small' | 'medium' | 'large';
}

export const ElevationDisplay: React.FC<ElevationDisplayProps> = ({
  elevationGain,
  elevationLoss,
  currentElevation,
  size = 'medium',
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, size);
  
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <View style={styles.item}>
          <Text style={styles.value}>+{elevationGain.toFixed(0)}</Text>
          <Text style={styles.label}>상승 (m)</Text>
        </View>
        {elevationLoss !== undefined && (
          <View style={styles.item}>
            <Text style={styles.value}>-{elevationLoss.toFixed(0)}</Text>
            <Text style={styles.label}>하강 (m)</Text>
          </View>
        )}
      </View>
      {currentElevation !== undefined && (
        <View style={styles.item}>
          <Text style={styles.currentValue}>{currentElevation.toFixed(0)}m</Text>
          <Text style={styles.label}>현재 고도</Text>
        </View>
      )}
    </View>
  );
};

const createStyles = (theme: Theme, size: string) => {
  const fontSize = size === 'small' 
    ? theme.typography.statSmall.fontSize
    : size === 'medium'
    ? theme.typography.statMedium.fontSize
    : theme.typography.statLarge.fontSize;
  
  return StyleSheet.create({
    container: {
      alignItems: 'center',
    },
    row: {
      flexDirection: 'row',
      gap: theme.spacing.md,
    },
    item: {
      alignItems: 'center',
    },
    value: {
      fontSize,
      fontWeight: '600',
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    currentValue: {
      fontSize: size === 'large' ? fontSize * 0.8 : fontSize,
      fontWeight: '600',
      color: theme.colors.primary,
      marginBottom: theme.spacing.xs,
    },
    label: {
      ...theme.typography.caption,
      color: theme.colors.textSecondary,
    },
  });
};

