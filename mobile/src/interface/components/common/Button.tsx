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
  const height = size === 'small' ? 36 : size === 'medium' ? 44 : 52;
  const paddingHorizontal = size === 'small' ? 16 : size === 'medium' ? 24 : 32;
  const fontSize = size === 'small' ? 14 : size === 'medium' ? 16 : 18;
  
  const getBackgroundColor = () => {
    if (variant === 'primary') return theme.colors.primary;
    if (variant === 'secondary') return theme.colors.secondary;
    return 'transparent';
  };
  
  const getTextColor = () => {
    if (variant === 'primary' || variant === 'secondary') {
      return theme.colors.textInverse;
    }
    return theme.colors.primary;
  };
  
  const getBorderColor = () => {
    if (variant === 'outline') return theme.colors.primary;
    return 'transparent';
  };
  
  return StyleSheet.create({
    button: {
      height,
      paddingHorizontal,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: getBackgroundColor(),
      borderWidth: variant === 'outline' ? 1 : 0,
      borderColor: getBorderColor(),
      width: fullWidth ? '100%' : undefined,
    },
    text: {
      fontSize,
      fontWeight: '600',
      color: getTextColor(),
    },
    disabled: {
      opacity: 0.5,
    },
  });
};

