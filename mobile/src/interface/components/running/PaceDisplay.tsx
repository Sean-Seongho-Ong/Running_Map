/**
 * PaceDisplay 컴포넌트
 * 페이스 전용 표시 컴포넌트
 */

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface PaceDisplayProps {
  pace: number; // 분/km
  size?: 'small' | 'medium' | 'large';
}

export const PaceDisplay: React.FC<PaceDisplayProps> = ({
  pace,
  size = 'medium',
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, size);
  
  const formatPace = (paceMinPerKm: number): string => {
    const minutes = Math.floor(paceMinPerKm);
    const seconds = Math.floor((paceMinPerKm - minutes) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };
  
  return (
    <View style={styles.container}>
      <Text style={styles.value}>{formatPace(pace)}</Text>
      <Text style={styles.label}>분/km</Text>
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
    value: {
      fontSize,
      fontWeight: '600',
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    label: {
      ...theme.typography.caption,
      color: theme.colors.textSecondary,
    },
  });
};

