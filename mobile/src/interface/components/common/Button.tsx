/**
 * Button 컴포넌트
 * Primary, Secondary, Outline, Text variants 지원
 */

import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator, ViewStyle, TextStyle } from 'react-native';
import { useTheme } from '../../hooks/useTheme';
import { Theme } from '../../../theme';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  style?: ViewStyle;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
  style,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, variant, size, fullWidth);
  
  return (
    <TouchableOpacity
      style={[styles.button, disabled && styles.disabled, style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator color={styles.text.color} />
      ) : (
        <Text style={styles.text}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

const createStyles = (
  theme: Theme,
  variant: string,
  size: string,
  fullWidth: boolean
) => {
  // Figma 디자인에 맞게 높이 조정: small 40px, medium 48px
  const height = size === 'small' ? 40 : size === 'medium' ? 48 : 52;
  const paddingHorizontal = size === 'small' ? 16 : size === 'medium' ? 24 : 32;
  const fontSize = size === 'small' ? 14 : size === 'medium' ? 16 : 18;
  
  const getBackgroundColor = () => {
    if (variant === 'primary') return theme.colors.primary;
    if (variant === 'secondary') return theme.colors.secondary;
    if (variant === 'outline') return theme.colors.surface; // outline 버튼은 흰색 배경
    return 'transparent';
  };
  
  const getTextColor = () => {
    if (variant === 'primary' || variant === 'secondary') {
      return theme.colors.textInverse;
    }
    // outline 버튼은 검은색 텍스트
    return theme.colors.text;
  };
  
  const getBorderColor = () => {
    if (variant === 'outline') return theme.colors.borderGray; // Figma 디자인: 회색 테두리
    return 'transparent';
  };
  
  return StyleSheet.create({
    button: {
      height,
      paddingHorizontal,
      borderRadius: 8, // Figma 디자인: 8px 모서리
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: getBackgroundColor(),
      borderWidth: variant === 'outline' ? 1 : 0,
      borderColor: getBorderColor(),
      width: fullWidth ? '100%' : undefined,
    },
    text: {
      fontSize,
      fontWeight: '600', // Semi Bold
      color: getTextColor(),
    },
    disabled: {
      opacity: 0.5,
    },
  });
};

