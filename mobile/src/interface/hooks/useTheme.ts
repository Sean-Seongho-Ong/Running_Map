/**
 * Theme Hook
 * 시스템 다크 모드 감지 및 Theme 제공
 */

import { useColorScheme } from 'react-native';
import { Theme, lightTheme, darkTheme } from '../../theme';

export const useTheme = (): Theme => {
  const colorScheme = useColorScheme();
  return colorScheme === 'dark' ? darkTheme : lightTheme;
};

