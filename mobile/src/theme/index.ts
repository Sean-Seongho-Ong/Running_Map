/**
 * Theme 시스템 통합
 * 다크 모드 지원
 */

import { colors } from './colors';
import { typography } from './typography';
import { spacing } from './spacing';

export interface Theme {
  colors: {
    primary: string;
    primaryDark: string;
    primaryLight: string;
    secondary: string;
    secondaryDark: string;
    secondaryLight: string;
    background: string;
    backgroundSecondary: string;
    surface: string;
    surfaceElevated: string;
    text: string;
    textSecondary: string;
    textDisabled: string;
    textInverse: string;
    border: string;
    borderLight: string;
    success: string;
    error: string;
    warning: string;
    info: string;
    dark: typeof colors.dark;
  };
  typography: typeof typography;
  spacing: typeof spacing;
  isDark: boolean;
}

export const lightTheme: Theme = {
  colors: {
    ...colors,
    // 다크 모드 색상은 별도로 관리
    dark: colors.dark,
  },
  typography,
  spacing,
  isDark: false,
};

export const darkTheme: Theme = {
  colors: {
    // Primary와 Secondary는 다크 모드에서도 유지
    primary: colors.primary,
    primaryDark: colors.primaryDark,
    primaryLight: colors.primaryLight,
    secondary: colors.secondary,
    secondaryDark: colors.secondaryDark,
    secondaryLight: colors.secondaryLight,
    // 다크 모드 배경 및 표면 색상
    background: colors.dark.background,
    backgroundSecondary: colors.dark.backgroundSecondary,
    surface: colors.dark.surface,
    surfaceElevated: colors.dark.surfaceElevated,
    // 다크 모드 텍스트 색상
    text: colors.dark.text,
    textSecondary: colors.dark.textSecondary,
    textDisabled: colors.dark.textDisabled,
    textInverse: colors.text, // 다크 모드에서는 밝은 텍스트
    // 다크 모드 테두리 색상
    border: colors.dark.border,
    borderLight: colors.dark.border,
    // Status 색상 유지
    success: colors.success,
    error: colors.error,
    warning: colors.warning,
    info: colors.info,
    // 다크 모드 색상 객체
    dark: colors.dark,
  },
  typography,
  spacing,
  isDark: true,
};

export { colors, typography, spacing };

