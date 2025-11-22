/**
 * Card 컴포넌트
 * 재사용 가능한 카드 컨테이너
 */

import React from 'react';
import { View, StyleSheet, ViewStyle, TouchableOpacity } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface CardProps {
  children: React.ReactNode;
  style?: ViewStyle;
  elevated?: boolean;
  onPress?: () => void;
}

export const Card: React.FC<CardProps> = ({
  children,
  style,
  elevated = false,
  onPress,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, elevated);
  
  if (onPress) {
    return (
      <TouchableOpacity
        style={[styles.card, style]}
        onPress={onPress}
        activeOpacity={0.7}
      >
        {children}
      </TouchableOpacity>
    );
  }
  
  return (
    <View style={[styles.card, style]}>
      {children}
    </View>
  );
};

const createStyles = (theme: Theme, elevated: boolean) =>
  StyleSheet.create({
    card: {
      backgroundColor: theme.colors.surface,
      borderRadius: 8, // Figma 디자인: 8px 모서리
      padding: theme.spacing.md,
      borderWidth: elevated ? 0 : 1, // elevated가 아닐 때 테두리 추가
      borderColor: theme.colors.border, // Figma 디자인: 회색 테두리
      ...(elevated && {
        shadowColor: '#000',
        shadowOffset: {
          width: 0,
          height: 2,
        },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
      }),
    },
  });

