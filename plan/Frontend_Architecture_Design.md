# 모바일 프론트엔드 아키텍처 상세 설계
## Running Map App - React Native

**문서 버전:** 1.0  
**작성일:** 2024  
**기술 스택:** React Native (TypeScript) + StyleSheet

---

## 1. 프로젝트 구조

### 1.1 전체 구조

```
mobile/
├── src/
│   ├── domain/                    # 비즈니스 로직 ✅ 구현 완료
│   │   ├── entities/
│   │   │   ├── Course.ts
│   │   │   └── RunningSession.ts
│   │   └── valueObjects/
│   │       ├── Coordinate.ts
│   │       └── Distance.ts
│   │
│   ├── application/               # 유즈케이스 (향후 구현)
│   │   ├── useCases/
│   │   │   ├── GenerateCourseUseCase.ts
│   │   │   ├── SaveCourseUseCase.ts
│   │   │   └── TrackRunningUseCase.ts
│   │   └── repositories/
│   │       ├── CourseRepository.ts
│   │       └── ApiRepository.ts
│   │
│   ├── infrastructure/            # 인프라스트럭처 (향후 구현)
│   │   ├── api/
│   │   │   ├── apiClient.ts
│   │   │   └── endpoints.ts
│   │   ├── storage/
│   │   │   └── AsyncStorage.ts
│   │   └── location/
│   │       └── LocationService.ts
│   │
│   ├── interface/                 # UI 계층 ✅ 구현 완료
│   │   ├── screens/
│   │   │   ├── MapScreen.tsx
│   │   │   ├── CourseGenerationScreen.tsx
│   │   │   ├── RunningScreen.tsx
│   │   │   └── CourseListScreen.tsx
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── map/
│   │   │   │   ├── MapView.tsx
│   │   │   │   ├── CoursePolyline.tsx
│   │   │   │   └── LocationMarker.tsx
│   │   │   └── running/
│   │   │       ├── RunningStats.tsx
│   │   │       ├── PaceDisplay.tsx
│   │   │       └── ElevationDisplay.tsx
│   │   ├── navigation/
│   │   │   └── AppNavigator.tsx
│   │   ├── hooks/
│   │   │   └── useTheme.ts
│   │   └── store/
│   │       ├── courseStore.ts
│   │       ├── runningStore.ts
│   │       └── locationStore.ts
│   │
│   └── theme/                      # 디자인 시스템 ✅ 구현 완료
│       ├── colors.ts
│       ├── typography.ts
│       ├── spacing.ts
│       └── index.ts
│
├── cursor-talk-to-figma-mcp/      # Figma MCP 통합 도구 ✅
│   ├── src/
│   │   ├── talk_to_figma_mcp/     # MCP 서버
│   │   ├── cursor_mcp_plugin/     # Figma 플러그인
│   │   └── socket.ts              # WebSocket 서버
│   └── readme.md
│
├── App.tsx                         # 앱 진입점 ✅
├── package.json                    # 의존성 관리 ✅
└── node_modules/                   # 설치된 패키지
```

**참고**: 
- `application/` 및 `infrastructure/` 폴더는 향후 구현 예정입니다.
- `ios/` 및 `android/` 폴더는 `expo run:ios` 또는 `expo run:android` 실행 시 자동 생성됩니다.
- `assets/`, `__tests__/` 폴더는 필요 시 추가됩니다.

---

## 2. Theme 시스템 (StyleSheet 기반)

### 2.1 Theme 구조

```typescript
// src/theme/colors.ts

export const colors = {
  // Primary Colors
  primary: '#FF6B35',        // 오렌지 (에너지, 러닝)
  primaryDark: '#E85A2B',
  primaryLight: '#FF8C5A',
  
  // Secondary Colors
  secondary: '#4ECDC4',      // 청록 (신선함)
  secondaryDark: '#3BA8A0',
  secondaryLight: '#6ED4CC',
  
  // Background
  background: '#FFFFFF',
  backgroundSecondary: '#F5F5F5',
  surface: '#FFFFFF',
  surfaceElevated: '#FAFAFA',
  
  // Text
  text: '#212121',
  textSecondary: '#757575',
  textDisabled: '#BDBDBD',
  textInverse: '#FFFFFF',
  
  // Border
  border: '#E0E0E0',
  borderLight: '#F5F5F5',
  
  // Status
  success: '#4CAF50',
  error: '#F44336',
  warning: '#FF9800',
  info: '#2196F3',
  
  // 다크 모드
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
};

// src/theme/typography.ts

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
};

// src/theme/spacing.ts

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// src/theme/index.ts

import { colors } from './colors';
import { typography } from './typography';
import { spacing } from './spacing';

export interface Theme {
  colors: typeof colors;
  typography: typeof typography;
  spacing: typeof spacing;
  isDark: boolean;
}

export const lightTheme: Theme = {
  colors: {
    ...colors,
    // 다크 모드 색상 제외
  },
  typography,
  spacing,
  isDark: false,
};

export const darkTheme: Theme = {
  colors: {
    ...colors.dark,
    primary: colors.primary,
    primaryDark: colors.primaryDark,
    primaryLight: colors.primaryLight,
    secondary: colors.secondary,
  },
  typography,
  spacing,
  isDark: true,
};

export { colors, typography, spacing };
```

### 2.2 Theme 사용 방법

```typescript
// hooks/useTheme.ts
import { useContext, createContext } from 'react';
import { lightTheme, darkTheme, Theme } from '../theme';
import { useColorScheme } from 'react-native';

const ThemeContext = createContext<Theme>(lightTheme);

export const useTheme = () => {
  const colorScheme = useColorScheme();
  const theme = colorScheme === 'dark' ? darkTheme : lightTheme;
  return theme;
};
```

---

## 3. 컴포넌트 설계

### 3.1 공통 컴포넌트

#### Button 컴포넌트

```typescript
// src/interface/components/common/Button.tsx

import React from 'react';
import { TouchableOpacity, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { useTheme } from '../../../hooks/useTheme';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'small' | 'medium' | 'large';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  disabled = false,
  loading = false,
  fullWidth = false,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, variant, size, fullWidth);
  
  return (
    <TouchableOpacity
      style={[styles.button, disabled && styles.disabled]}
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
  
  return StyleSheet.create({
    button: {
      height,
      paddingHorizontal,
      borderRadius: 8,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: variant === 'primary' 
        ? theme.colors.primary 
        : variant === 'secondary'
        ? theme.colors.secondary
        : variant === 'outline'
        ? 'transparent'
        : 'transparent',
      borderWidth: variant === 'outline' ? 1 : 0,
      borderColor: theme.colors.primary,
      width: fullWidth ? '100%' : undefined,
    },
    text: {
      fontSize,
      fontWeight: '600',
      color: variant === 'primary' || variant === 'secondary'
        ? theme.colors.textInverse
        : theme.colors.primary,
    },
    disabled: {
      opacity: 0.5,
    },
  });
};
```

#### Input 컴포넌트

```typescript
// src/interface/components/common/Input.tsx

import React from 'react';
import { TextInput, View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../../hooks/useTheme';

interface InputProps {
  label?: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  keyboardType?: 'default' | 'numeric' | 'decimal-pad';
  error?: string;
  disabled?: boolean;
}

export const Input: React.FC<InputProps> = ({
  label,
  value,
  onChangeText,
  placeholder,
  keyboardType = 'default',
  error,
  disabled = false,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme, !!error);
  
  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}
      <TextInput
        style={[styles.input, error && styles.inputError]}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        placeholderTextColor={theme.colors.textDisabled}
        keyboardType={keyboardType}
        editable={!disabled}
      />
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};

const createStyles = (theme: Theme, hasError: boolean) =>
  StyleSheet.create({
    container: {
      marginBottom: theme.spacing.md,
    },
    label: {
      ...theme.typography.captionBold,
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    input: {
      ...theme.typography.body,
      height: 48,
      paddingHorizontal: theme.spacing.md,
      backgroundColor: theme.colors.surface,
      borderWidth: 1,
      borderColor: hasError ? theme.colors.error : theme.colors.border,
      borderRadius: 8,
      color: theme.colors.text,
    },
    inputError: {
      borderColor: theme.colors.error,
    },
    errorText: {
      ...theme.typography.caption,
      color: theme.colors.error,
      marginTop: theme.spacing.xs,
    },
  });
```

### 3.2 지도 컴포넌트

#### MapView 컴포넌트

```typescript
// src/interface/components/map/MapView.tsx

import React, { useRef } from 'react';
import MapView, { PROVIDER_DEFAULT, Polyline, Marker } from 'react-native-maps';
import { StyleSheet, View } from 'react-native';
import { Coordinate } from '../../../domain/valueObjects/Coordinate';

interface MapViewProps {
  initialLocation: Coordinate;
  coursePolyline?: Coordinate[];
  currentLocation?: Coordinate;
  onRegionChange?: (region: any) => void;
}

export const CustomMapView: React.FC<MapViewProps> = ({
  initialLocation,
  coursePolyline,
  currentLocation,
  onRegionChange,
}) => {
  const mapRef = useRef<MapView>(null);
  
  return (
    <View style={styles.container}>
      <MapView
        ref={mapRef}
        provider={PROVIDER_DEFAULT}
        style={styles.map}
        initialRegion={{
          latitude: initialLocation.latitude,
          longitude: initialLocation.longitude,
          latitudeDelta: 0.01,
          longitudeDelta: 0.01,
        }}
        customMapStyle={[]} // OSM 타일 사용 시
        urlTemplate="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        onRegionChangeComplete={onRegionChange}
      >
        {/* 현재 위치 마커 */}
        {currentLocation && (
          <Marker
            coordinate={{
              latitude: currentLocation.latitude,
              longitude: currentLocation.longitude,
            }}
            title="현재 위치"
            pinColor="#FF6B35"
          />
        )}
        
        {/* 코스 폴리라인 */}
        {coursePolyline && coursePolyline.length > 0 && (
          <Polyline
            coordinates={coursePolyline.map(coord => ({
              latitude: coord.latitude,
              longitude: coord.longitude,
            }))}
            strokeColor="#FF6B35"
            strokeWidth={4}
          />
        )}
      </MapView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
});
```

### 3.3 러닝 통계 컴포넌트

#### RunningStats 컴포넌트

```typescript
// src/interface/components/running/RunningStats.tsx

import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useTheme } from '../../../hooks/useTheme';

interface RunningStatsProps {
  distance: number;      // km
  duration: number;      // 초
  pace: number;         // 분/km
  speed: number;        // km/h
  elevationGain: number; // m
}

export const RunningStats: React.FC<RunningStatsProps> = ({
  distance,
  duration,
  pace,
  speed,
  elevationGain,
}) => {
  const theme = useTheme();
  const styles = createStyles(theme);
  
  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };
  
  const formatPace = (paceMinPerKm: number): string => {
    const minutes = Math.floor(paceMinPerKm);
    const seconds = Math.floor((paceMinPerKm - minutes) * 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };
  
  return (
    <View style={styles.container}>
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{distance.toFixed(2)}</Text>
          <Text style={styles.statLabel}>거리 (km)</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{formatTime(duration)}</Text>
          <Text style={styles.statLabel}>시간</Text>
        </View>
      </View>
      
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{formatPace(pace)}</Text>
          <Text style={styles.statLabel}>페이스 (분/km)</Text>
        </View>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{speed.toFixed(1)}</Text>
          <Text style={styles.statLabel}>속도 (km/h)</Text>
        </View>
      </View>
      
      <View style={styles.row}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>+{elevationGain.toFixed(0)}</Text>
          <Text style={styles.statLabel}>고저차 (m)</Text>
        </View>
      </View>
    </View>
  );
};

const createStyles = (theme: Theme) =>
  StyleSheet.create({
    container: {
      backgroundColor: theme.colors.surface,
      padding: theme.spacing.md,
      borderRadius: 12,
    },
    row: {
      flexDirection: 'row',
      justifyContent: 'space-around',
      marginBottom: theme.spacing.md,
    },
    statItem: {
      alignItems: 'center',
      flex: 1,
    },
    statValue: {
      ...theme.typography.statMedium,
      color: theme.colors.text,
      marginBottom: theme.spacing.xs,
    },
    statLabel: {
      ...theme.typography.caption,
      color: theme.colors.textSecondary,
    },
  });
```

---

## 4. 상태 관리 (Zustand)

### 4.1 Course Store

```typescript
// src/interface/store/courseStore.ts

import { create } from 'zustand';
import { Course } from '../../domain/entities/Course';
import { Coordinate } from '../../domain/valueObjects/Coordinate';
import { Distance } from '../../domain/valueObjects/Distance';
import { CourseRepository } from '../../application/repositories/CourseRepository';

interface CourseStore {
  // State
  courses: Course[];
  selectedCourse: Course | null;
  generatedCourse: Course | null;
  isGenerating: boolean;
  generationError: string | null;
  
  // Actions
  generateCourse: (
    startPoint: Coordinate,
    targetDistance: Distance,
    parameters?: any
  ) => Promise<void>;
  selectCourse: (courseId: string) => void;
  saveCourse: (course: Course, name: string) => Promise<void>;
  loadCourses: () => Promise<void>;
  clearGeneratedCourse: () => void;
}

export const useCourseStore = create<CourseStore>((set, get) => ({
  courses: [],
  selectedCourse: null,
  generatedCourse: null,
  isGenerating: false,
  generationError: null,
  
  generateCourse: async (startPoint, targetDistance, parameters) => {
    set({ isGenerating: true, generationError: null });
    try {
      const repository = new CourseRepository();
      const course = await repository.generateCourse(
        startPoint,
        targetDistance,
        parameters
      );
      set({ generatedCourse: course, isGenerating: false });
    } catch (error) {
      set({
        generationError: error.message,
        isGenerating: false,
      });
    }
  },
  
  selectCourse: (courseId) => {
    const course = get().courses.find(c => c.id === courseId);
    set({ selectedCourse: course || null });
  },
  
  saveCourse: async (course, name) => {
    const repository = new CourseRepository();
    const savedCourse = await repository.saveCourse({ ...course, name });
    set(state => ({
      courses: [...state.courses, savedCourse],
    }));
  },
  
  loadCourses: async () => {
    const repository = new CourseRepository();
    const courses = await repository.loadCourses();
    set({ courses });
  },
  
  clearGeneratedCourse: () => {
    set({ generatedCourse: null });
  },
}));
```

### 4.2 Running Store

```typescript
// src/interface/store/runningStore.ts

import { create } from 'zustand';
import { RunningSession } from '../../domain/entities/RunningSession';
import { Coordinate } from '../../domain/valueObjects/Coordinate';
import { RunningService } from '../../domain/services/RunningService';

interface RunningStore {
  // State
  session: RunningSession | null;
  isRunning: boolean;
  isPaused: boolean;
  currentLocation: Coordinate | null;
  stats: {
    distance: number;
    duration: number;
    pace: number;
    speed: number;
    elevationGain: number;
  };
  
  // Actions
  startRunning: (courseId?: string) => Promise<void>;
  pauseRunning: () => void;
  resumeRunning: () => void;
  updateLocation: (location: Coordinate) => void;
  finishRunning: () => Promise<RunningSession>;
  reset: () => void;
}

export const useRunningStore = create<RunningStore>((set, get) => ({
  session: null,
  isRunning: false,
  isPaused: false,
  currentLocation: null,
  stats: {
    distance: 0,
    duration: 0,
    pace: 0,
    speed: 0,
    elevationGain: 0,
  },
  
  startRunning: async (courseId) => {
    const service = new RunningService();
    const session = await service.startSession(courseId);
    set({
      session,
      isRunning: true,
      isPaused: false,
      stats: {
        distance: 0,
        duration: 0,
        pace: 0,
        speed: 0,
        elevationGain: 0,
      },
    });
  },
  
  pauseRunning: () => {
    set({ isPaused: true, isRunning: false });
  },
  
  resumeRunning: () => {
    set({ isPaused: false, isRunning: true });
  },
  
  updateLocation: (location) => {
    const service = new RunningService();
    const stats = service.calculateStats(
      get().session?.locations || [],
      location
    );
    set({
      currentLocation: location,
      stats,
    });
  },
  
  finishRunning: async () => {
    const service = new RunningService();
    const session = get().session;
    if (!session) throw new Error('No active session');
    
    const finishedSession = await service.finishSession(session);
    set({
      session: finishedSession,
      isRunning: false,
      isPaused: false,
    });
    return finishedSession;
  },
  
  reset: () => {
    set({
      session: null,
      isRunning: false,
      isPaused: false,
      currentLocation: null,
      stats: {
        distance: 0,
        duration: 0,
        pace: 0,
        speed: 0,
        elevationGain: 0,
      },
    });
  },
}));
```

---

## 5. 네비게이션 구조

### 5.1 AppNavigator

```typescript
// src/interface/navigation/AppNavigator.tsx

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { MapScreen } from '../screens/MapScreen';
import { CourseListScreen } from '../screens/CourseListScreen';
import { CourseGenerationScreen } from '../screens/CourseGenerationScreen';
import { RunningScreen } from '../screens/RunningScreen';
import { useTheme } from '../../hooks/useTheme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const MapStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Map"
      component={MapScreen}
      options={{ headerShown: false }}
    />
    <Stack.Screen
      name="CourseGeneration"
      component={CourseGenerationScreen}
      options={{ title: '코스 생성' }}
    />
  </Stack.Navigator>
);

const CoursesStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="CourseList"
      component={CourseListScreen}
      options={{ title: '내 코스' }}
    />
  </Stack.Navigator>
);

const RunningStack = () => (
  <Stack.Navigator>
    <Stack.Screen
      name="Running"
      component={RunningScreen}
      options={{ headerShown: false }}
    />
  </Stack.Navigator>
);

export const AppNavigator = () => {
  const theme = useTheme();
  
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={{
          tabBarActiveTintColor: theme.colors.primary,
          tabBarInactiveTintColor: theme.colors.textSecondary,
          headerStyle: {
            backgroundColor: theme.colors.surface,
          },
          headerTintColor: theme.colors.text,
        }}
      >
        <Tab.Screen
          name="MapTab"
          component={MapStack}
          options={{ title: '지도', tabBarLabel: '지도' }}
        />
        <Tab.Screen
          name="CoursesTab"
          component={CoursesStack}
          options={{ title: '코스', tabBarLabel: '코스' }}
        />
        <Tab.Screen
          name="RunningTab"
          component={RunningStack}
          options={{ title: '러닝', tabBarLabel: '러닝' }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
};
```

---

## 6. 주요 화면 구현 가이드

### 6.1 MapScreen

**주요 기능:**
- 지도 표시
- 현재 위치 표시
- 코스 생성 버튼
- 저장된 코스 표시

**구현 포인트:**
- 지도는 전체 화면의 70% 차지
- 하단에 액션 버튼 배치
- 현재 위치는 자동으로 중심에 배치

### 6.2 CourseGenerationScreen

**주요 기능:**
- 거리 입력
- 코스 생성 요청
- 생성 진행 상태 표시
- 생성된 코스 미리보기

**구현 포인트:**
- 지도와 입력 영역을 분리
- 프리셋 버튼으로 빠른 입력
- 로딩 상태 명확히 표시

### 6.3 RunningScreen

**주요 기능:**
- 러닝 통계 실시간 표시
- 지도에 현재 경로 표시
- 일시정지/재개/종료 버튼

**구현 포인트:**
- 러닝 중에는 큰 폰트로 통계 표시
- 버튼은 하단 중앙 배치
- 실수 방지를 위한 확인 다이얼로그

---

## 7. 스타일링 가이드라인

### 7.1 StyleSheet 사용 원칙

1. **Theme 객체 활용**
   - 모든 색상, 폰트, 간격은 theme에서 가져오기
   - 하드코딩 금지

2. **스타일 재사용**
   - 공통 스타일은 별도 파일로 분리
   - 컴포넌트별 스타일은 해당 파일 내부에 정의

3. **조건부 스타일**
   - `StyleSheet.flatten()` 사용
   - 배열로 여러 스타일 조합

### 7.2 반응형 디자인

- `Dimensions` API로 화면 크기 감지
- 작은 화면과 큰 화면 대응
- 세로/가로 모드 대응

---

## 8. 성능 최적화

### 8.1 리렌더링 최적화

- `React.memo`로 불필요한 리렌더링 방지
- `useMemo`, `useCallback` 활용
- Zustand의 선택적 구독

### 8.2 지도 성능

- 폴리라인 단순화 (Douglas-Peucker)
- 마커 클러스터링 (많은 마커 시)
- 지도 영역만 업데이트

---

## 9. 접근성

### 9.1 스크린 리더 지원

- `accessibilityLabel` 설정
- `accessibilityHint` 제공
- `accessibilityRole` 명시

### 9.2 터치 영역

- 최소 44x44pt 보장
- 터치 피드백 제공

---

## 10. 다음 단계

### 즉시 진행할 작업

1. **Expo Bare Workflow 프로젝트 초기화**
   ```bash
   npx create-expo-app@latest RunningMapApp --template bare
   cd RunningMapApp
   ```
   
   **또는 기존 Expo 프로젝트를 Bare로 전환:**
   ```bash
   npx expo eject
   ```

2. **필수 라이브러리 설치**
   ```bash
   npm install react-native-maps @react-navigation/native @react-navigation/bottom-tabs @react-navigation/stack zustand @react-native-community/geolocation
   
   # iOS 의존성 설치 (iOS만)
   cd ios && pod install && cd ..
   ```

3. **Expo Dev Client 설정**
   ```bash
   npx expo install expo-dev-client
   ```
   
   **개발 빌드 생성:**
   ```bash
   # Android
   npx expo run:android
   
   # iOS
   npx expo run:ios
   ```

3. **Theme 시스템 구현**
   - `src/theme/` 폴더 생성
   - colors, typography, spacing 파일 작성

4. **기본 컴포넌트 구현**
   - Button, Input 등 공통 컴포넌트
   - MapView 컴포넌트

5. **Figma 와이어프레임 작성**
   - 핵심 화면 4개
   - 기본 디자인 시스템

---

**프로세스 B로 빠르게 시작하여 개발과 병행하며 지속적으로 개선합니다.**

