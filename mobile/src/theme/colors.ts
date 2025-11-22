/**
 * 색상 팔레트 정의
 * Material Design 및 Human Interface Guidelines 참고
 */

export const colors = {
  // Primary Colors - 러닝 앱 특성에 맞는 활기찬 색상
  primary: '#FF6B35',        // 오렌지 (에너지, 러닝)
  primaryDark: '#E85A2B',
  primaryLight: '#FF8C5A',
  
  // Secondary Colors
  secondary: '#4ECDC4',        // 청록 (신선함)
  secondaryDark: '#3BA8A0',
  secondaryLight: '#6ED4CC',
  
  // Background Colors
  background: '#FFFFFF',
  backgroundSecondary: '#F5F5F5',
  surface: '#FFFFFF',
  surfaceElevated: '#FAFAFA',
  surfaceLight: '#FAFAFA',        // Figma 디자인: Input Container 배경
  mapBackground: '#D9D9D9',      // Figma 디자인: 지도 영역 배경
  
  // Text Colors
  text: '#212121',
  textSecondary: '#757575',
  textDisabled: '#BDBDBD',
  textInverse: '#FFFFFF',
  
  // Border Colors
  border: '#E0E0E0',
  borderLight: '#F5F5F5',
  borderGray: '#E0E0E0',         // Figma 디자인: outline 버튼 테두리 (RGB: 0.88, 0.88, 0.88)
  
  // Status Colors
  success: '#4CAF50',
  error: '#F44336',
  warning: '#FF9800',
  info: '#2196F3',
  
  // 다크 모드 색상
  dark: {
    background: '#121212',
    backgroundSecondary: '#1E1E1E',
    surface: '#1E1E1E',
    surfaceElevated: '#2C2C2C',
    text: '#FFFFFF',
    textSecondary: '#B0B0B0',
    textDisabled: '#666666',
    border: '#333333',
  },
} as const;

