/**
 * 타이포그래피 시스템 정의
 * 시스템 폰트 활용 (San Francisco, Roboto)
 */

export const typography = {
  // Headings
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 40,
    letterSpacing: -0.5,
  },
  h2: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
    letterSpacing: -0.3,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 28,
  },
  
  // Body
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  bodyBold: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 24,
  },
  
  // Caption
  caption: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 20,
  },
  captionBold: {
    fontSize: 14,
    fontWeight: '600' as const,
    lineHeight: 20,
  },
  
  // Small
  small: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 16,
  },
  
  // 러닝 통계용 큰 폰트
  statLarge: {
    fontSize: 48,
    fontWeight: '700' as const,
    lineHeight: 56,
  },
  statMedium: {
    fontSize: 32,
    fontWeight: '600' as const,
    lineHeight: 40,
  },
  statSmall: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
  },
} as const;

