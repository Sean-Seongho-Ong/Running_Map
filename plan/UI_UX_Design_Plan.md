# 모바일 프론트엔드 및 UX/UI 설계 계획
## Running Map App

**작성일:** 2024  
**목적:** 모바일 앱의 프론트엔드 아키텍처 및 UX/UI 설계 방법론 정의

---

## 1. UX/UI 설계 방법론

### 1.1 설계 프로세스

#### Phase 1: 사용자 연구 및 요구사항 분석
1. **사용자 페르소나 정의**
   - 주요 사용자 그룹 식별
   - 사용자 니즈 및 목표 정의
   - 사용 시나리오 작성

2. **사용자 여정 맵 (User Journey Map)**
   - 코스 생성 여정
   - 러닝 추적 여정
   - 코스 탐색 여정

3. **기능 우선순위 정의**
   - Must Have / Should Have / Nice to Have
   - MVP 기능 선정

#### Phase 2: 정보 아키텍처 (IA) 설계
1. **화면 구조 설계**
   - 주요 화면 목록
   - 화면 간 네비게이션 흐름
   - 정보 계층 구조

2. **사용자 플로우 다이어그램**
   - 코스 생성 플로우
   - 러닝 시작 플로우
   - 코스 저장/로드 플로우

#### Phase 3: 와이어프레임 설계
1. **로우파이 와이어프레임**
   - 각 화면의 기본 레이아웃
   - UI 요소 배치
   - 정보 우선순위

2. **도구 선택**
   - Figma (권장)
   - Sketch
   - Adobe XD

#### Phase 4: 프로토타입 설계
1. **하이파이 프로토타입**
   - 실제 디자인 적용
   - 인터랙션 정의
   - 애니메이션 설계

2. **프로토타입 테스트**
   - 사용성 테스트
   - 피드백 수집

#### Phase 5: 디자인 시스템 구축
1. **디자인 토큰 정의**
   - 색상 팔레트
   - 타이포그래피
   - 간격 시스템
   - 아이콘 시스템

2. **컴포넌트 라이브러리**
   - 재사용 가능한 UI 컴포넌트
   - 상태별 변형 정의

---

## 2. 프론트엔드 아키텍처 설계

### 2.1 컴포넌트 계층 구조

```
interface/
├── screens/              # 화면 컴포넌트
│   ├── MapScreen.tsx
│   ├── CourseGenerationScreen.tsx
│   ├── RunningScreen.tsx
│   └── CourseListScreen.tsx
│
├── components/           # 재사용 가능한 컴포넌트
│   ├── common/          # 공통 컴포넌트
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── Loading.tsx
│   ├── map/             # 지도 관련 컴포넌트
│   │   ├── MapView.tsx
│   │   ├── CoursePolyline.tsx
│   │   └── LocationMarker.tsx
│   ├── course/          # 코스 관련 컴포넌트
│   │   ├── CourseCard.tsx
│   │   ├── CourseInfo.tsx
│   │   └── CourseList.tsx
│   └── running/         # 러닝 관련 컴포넌트
│       ├── RunningStats.tsx
│       ├── PaceDisplay.tsx
│       └── ElevationChart.tsx
│
├── layouts/             # 레이아웃 컴포넌트
│   ├── ScreenLayout.tsx
│   └── TabLayout.tsx
│
└── hooks/               # 커스텀 훅
    ├── useLocation.ts
    ├── useCourseGeneration.ts
    └── useRunningTracker.ts
```

### 2.2 상태 관리 설계

**Zustand 스토어 구조:**

```typescript
// store/useStore.ts

interface AppState {
  // 위치 상태
  currentLocation: Coordinate | null;
  locationPermission: PermissionStatus;
  
  // 코스 상태
  generatedCourse: Course | null;
  selectedCourse: Course | null;
  courseList: Course[];
  isGenerating: boolean;
  
  // 러닝 상태
  runningSession: RunningSession | null;
  isRunning: boolean;
  runningStats: RunningStats;
  
  // UI 상태
  theme: 'light' | 'dark';
  activeTab: string;
}
```

### 2.3 네비게이션 설계

**React Navigation 구조:**

```
AppNavigator
├── AuthNavigator (향후)
│
└── MainNavigator
    ├── TabNavigator
    │   ├── MapTab
    │   │   └── MapScreen
    │   ├── CoursesTab
    │   │   └── CourseListScreen
    │   └── ProfileTab (향후)
    │
    └── StackNavigator
        ├── CourseGenerationScreen
        ├── CourseDetailScreen
        ├── RunningScreen
        └── RunningResultScreen
```

---

## 3. 주요 화면 설계

### 3.1 MapScreen (메인 화면)

**기능:**
- 지도 표시
- 현재 위치 표시
- 코스 생성 버튼
- 저장된 코스 표시

**레이아웃:**
```
┌─────────────────────────┐
│  [메뉴]  Running Map    │ ← 헤더
├─────────────────────────┤
│                         │
│        지도 영역         │
│                         │
│                         │
├─────────────────────────┤
│ [코스 생성] [코스 목록] │ ← 하단 버튼
└─────────────────────────┘
```

### 3.2 CourseGenerationScreen

**기능:**
- 거리 입력
- 코스 생성 요청
- 생성 진행 상태 표시
- 생성된 코스 미리보기

**레이아웃:**
```
┌─────────────────────────┐
│  ← 뒤로    코스 생성     │
├─────────────────────────┤
│                         │
│        지도 영역         │
│   (생성된 코스 표시)      │
│                         │
├─────────────────────────┤
│ 목표 거리: [10.0] km    │
│ [5km] [10km] [15km]     │ ← 프리셋 버튼
│                         │
│ [코스 생성하기]          │
│                         │
│ 생성 중... (진행률 표시) │
└─────────────────────────┘
```

### 3.3 RunningScreen

**기능:**
- 러닝 통계 실시간 표시
- 지도에 현재 경로 표시
- 일시정지/재개/종료 버튼

**레이아웃:**
```
┌─────────────────────────┐
│                         │
│        지도 영역         │
│   (현재 경로 표시)        │
│                         │
├─────────────────────────┤
│ 거리: 5.2 km            │
│ 시간: 00:30:15           │
│ 페이스: 5:50 /km         │
│ 속도: 10.2 km/h          │
│ 고저차: +120m            │
├─────────────────────────┤
│ [일시정지] [종료]        │
└─────────────────────────┘
```

### 3.4 CourseListScreen

**기능:**
- 코스 목록 표시
- 검색 기능
- 코스 선택 및 상세 보기

**레이아웃:**
```
┌─────────────────────────┐
│  [검색]                 │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ 한강 러닝 코스       │ │
│ │ 10.0 km • 평지      │ │
│ │ 생성일: 2024-01-01  │ │
│ └─────────────────────┘ │
│                         │
│ ┌─────────────────────┐ │
│ │ 올림픽공원 코스      │ │
│ │ 5.0 km • 언덕        │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

---

## 4. 디자인 시스템

### 4.1 색상 팔레트

**기본 색상:**
- Primary: 러닝 테마 색상 (예: #FF6B35 오렌지, #4ECDC4 청록)
- Secondary: 보조 색상
- Background: 배경색
- Surface: 카드/컨테이너 배경
- Text: 텍스트 색상
- Error: 에러 색상
- Success: 성공 색상

**다크 모드:**
- 각 색상의 다크 모드 변형 정의

### 4.2 타이포그래피

**폰트 스케일:**
- H1: 32px (화면 제목)
- H2: 24px (섹션 제목)
- H3: 20px (서브 제목)
- Body: 16px (본문)
- Caption: 14px (설명)
- Small: 12px (작은 텍스트)

**폰트 웨이트:**
- Regular: 400
- Medium: 500
- SemiBold: 600
- Bold: 700

### 4.3 간격 시스템

**8px 그리드 시스템:**
- XS: 4px
- S: 8px
- M: 16px
- L: 24px
- XL: 32px
- XXL: 48px

### 4.4 컴포넌트 스타일

**버튼:**
- Primary Button: 주요 액션
- Secondary Button: 보조 액션
- Text Button: 텍스트 버튼
- Icon Button: 아이콘 버튼

**입력 필드:**
- Text Input
- Number Input
- Search Input

**카드:**
- Course Card
- Stats Card

---

## 5. 인터랙션 설계

### 5.1 애니메이션

1. **화면 전환**
   - 슬라이드 애니메이션
   - 페이드 애니메이션

2. **로딩 상태**
   - 스켈레톤 로딩
   - 프로그레스 인디케이터

3. **피드백**
   - 버튼 터치 피드백
   - 성공/실패 토스트 메시지

### 5.2 제스처

- **스와이프**: 코스 카드 삭제
- **핀치 줌**: 지도 확대/축소
- **롱 프레스**: 컨텍스트 메뉴

### 5.3 접근성

- **스크린 리더 지원**: React Native Accessibility API
- **색상 대비**: WCAG 2.1 AA 준수
- **터치 영역**: 최소 44x44pt

---

## 6. 설계 도구 및 방법

### 6.1 추천 도구

#### 옵션 1: Figma (권장)
**장점:**
- 협업 기능 우수
- 컴포넌트 시스템 구축 용이
- 프로토타입 기능 강력
- 무료 플랜 제공

**사용 방법:**
1. 와이어프레임 작성
2. 디자인 시스템 구축
3. 하이파이 프로토타입 제작
4. 개발자 핸오프

#### 옵션 2: Pen & Paper + Figma
**장점:**
- 빠른 아이디어 스케치
- 비용 없음
- 자유로운 표현

**사용 방법:**
1. 페이퍼 스케치
2. Figma로 디지털화
3. 프로토타입 제작

#### 옵션 3: 직접 코딩 (Design in Code)
**장점:**
- 빠른 반복
- 실제 구현과 동일
- 개발 시간 단축

**단점:**
- 디자인 품질 제한
- 재작업 가능성

### 6.2 설계 단계별 산출물

1. **Phase 1 산출물**
   - 사용자 페르소나 문서
   - 사용자 여정 맵
   - 기능 우선순위 매트릭스

2. **Phase 2 산출물**
   - 정보 아키텍처 다이어그램
   - 사용자 플로우 다이어그램
   - 화면 목록

3. **Phase 3 산출물**
   - 로우파이 와이어프레임 (Figma)
   - 화면별 레이아웃 스펙

4. **Phase 4 산출물**
   - 하이파이 프로토타입 (Figma)
   - 인터랙션 스펙
   - 애니메이션 가이드

5. **Phase 5 산출물**
   - 디자인 시스템 문서
   - 컴포넌트 라이브러리
   - 스타일 가이드

---

## 7. 권장 설계 프로세스

### 프로세스 A: 전통적 디자인 프로세스 (권장)

```
1. 사용자 연구 (1주)
   ↓
2. 정보 아키텍처 설계 (3일)
   ↓
3. 와이어프레임 작성 (1주)
   ↓
4. 프로토타입 제작 (1주)
   ↓
5. 사용성 테스트 (3일)
   ↓
6. 디자인 시스템 구축 (1주)
   ↓
7. 개발 핸오프 (3일)
```

**총 소요 시간:** 약 5-6주

**장점:**
- 체계적인 설계
- 사용자 피드백 반영 가능
- 일관된 디자인

**단점:**
- 시간 소요
- 초기 비용

---

### 프로세스 B: 빠른 프로토타이핑 (MVP)

```
1. 핵심 화면 와이어프레임 (3일)
   ↓
2. 간단한 프로토타입 (3일)
   ↓
3. 기본 디자인 시스템 (2일)
   ↓
4. 개발 시작 (동시 진행)
   ↓
5. 반복적 개선
```

**총 소요 시간:** 약 1-2주

**장점:**
- 빠른 시작
- 빠른 피드백
- 비용 절감

**단점:**
- 재작업 가능성
- 일관성 부족 가능

---

### 프로세스 C: 하이브리드 접근 (권장)

```
1. 핵심 화면만 상세 설계 (1주)
   - MapScreen
   - CourseGenerationScreen
   - RunningScreen
   ↓
2. 기본 디자인 시스템 구축 (3일)
   ↓
3. 개발 시작 (동시 진행)
   ↓
4. 나머지 화면은 개발 중 설계
   ↓
5. 지속적 개선
```

**총 소요 시간:** 약 2주 (초기)

**장점:**
- 빠른 시작 + 체계적 접근
- 핵심 기능 집중
- 유연한 변경

---

## 8. 구체적인 설계 방법 제안

### 8.1 현재 프로젝트에 적합한 방법

**추천: 프로세스 C (하이브리드 접근)**

**이유:**
- MVP 빠른 출시 필요
- 핵심 기능에 집중
- 개발과 병행 가능

**실행 계획:**

**Week 1: 핵심 설계**
1. **사용자 플로우 정의** (1일)
   - 코스 생성 플로우
   - 러닝 추적 플로우
   - 코스 탐색 플로우

2. **핵심 화면 와이어프레임** (2일)
   - MapScreen
   - CourseGenerationScreen
   - RunningScreen
   - 도구: Figma 또는 페이퍼 스케치

3. **기본 디자인 시스템** (2일)
   - 색상 팔레트
   - 타이포그래피
   - 기본 컴포넌트 스타일

**Week 2: 프로토타입 및 개발 시작**
1. **하이파이 프로토타입** (2일)
   - 핵심 화면만
   - 기본 인터랙션

2. **디자인 시스템 문서화** (1일)
   - 스타일 가이드 작성

3. **개발 시작** (동시 진행)
   - 컴포넌트 구조 설정
   - 기본 레이아웃 구현

**개발 중:**
- 나머지 화면 설계
- 컴포넌트 상세 설계
- 지속적 개선

### 8.2 설계 도구 선택

**추천: Figma**

**이유:**
- 무료 플랜 제공
- 협업 용이
- 컴포넌트 시스템 구축 가능
- 개발자 핸오프 용이

**대안:**
- **Excalidraw**: 빠른 스케치용
- **Pen & Paper**: 초기 아이디어용

---

## 9. 프론트엔드 아키텍처 상세 설계

### 9.1 컴포넌트 설계 원칙

1. **원자적 디자인 (Atomic Design)**
   - Atoms: 기본 요소 (Button, Input)
   - Molecules: 조합 요소 (SearchBar, CourseCard)
   - Organisms: 복합 요소 (CourseList, RunningStats)
   - Templates: 레이아웃
   - Pages: 화면

2. **컴포넌트 재사용성**
   - Props를 통한 커스터마이징
   - 컴포넌트 조합
   - 스타일 변형 지원

3. **관심사 분리**
   - Presentation Component: UI만 담당
   - Container Component: 로직 담당
   - Custom Hooks: 비즈니스 로직 분리

### 9.2 상태 관리 전략

**Zustand 스토어 구조:**

```typescript
// store/courseStore.ts
interface CourseStore {
  // State
  courses: Course[];
  selectedCourse: Course | null;
  isGenerating: boolean;
  
  // Actions
  generateCourse: (params: GenerateParams) => Promise<void>;
  selectCourse: (courseId: string) => void;
  saveCourse: (course: Course) => Promise<void>;
}

// store/runningStore.ts
interface RunningStore {
  // State
  session: RunningSession | null;
  isRunning: boolean;
  stats: RunningStats;
  
  // Actions
  startRunning: (courseId?: string) => Promise<void>;
  updateLocation: (location: Coordinate) => void;
  pauseRunning: () => void;
  finishRunning: () => Promise<void>;
}
```

### 9.3 스타일링 전략

**옵션 1: StyleSheet (React Native 기본)**
- 성능 우수
- 타입 안정성
- 기본 제공

**옵션 2: styled-components**
- CSS-in-JS
- 동적 스타일링
- 테마 지원

**옵션 3: Tailwind CSS (NativeWind)**
- 유틸리티 퍼스트
- 빠른 개발
- 일관된 스타일

**권장: StyleSheet + Theme 객체**
- 성능과 개발 편의성 균형
- 타입 안정성
- 다크 모드 지원 용이

---

## 10. UX 고려사항

### 10.1 러닝 중 사용성

**제약사항:**
- 한 손 조작 가능해야 함
- 큰 버튼 크기 (최소 44x44pt)
- 명확한 피드백
- 실수 방지 (종료 버튼 확인)

**디자인 원칙:**
- 중요한 정보는 상단 배치
- 통계는 큰 폰트로 표시
- 버튼은 하단 중앙 배치
- 색상으로 상태 구분

### 10.2 오프라인 고려

- 오프라인 상태 표시
- 저장된 코스는 오프라인에서도 조회
- 네트워크 오류 시 명확한 메시지

### 10.3 배터리 최적화

- 지도 업데이트 최소화
- GPS 업데이트 주기 조정
- 다크 모드 제공 (OLED 절약)

---

## 11. 다음 단계

### 즉시 진행 가능한 작업

1. **사용자 플로우 다이어그램 작성**
   - 코스 생성 플로우
   - 러닝 추적 플로우

2. **핵심 화면 와이어프레임 작성**
   - Figma 또는 페이퍼 스케치
   - 3개 핵심 화면

3. **기본 디자인 시스템 정의**
   - 색상 팔레트
   - 타이포그래피
   - 간격 시스템

4. **프론트엔드 프로젝트 구조 생성**
   - React Native 프로젝트 초기화
   - 폴더 구조 생성
   - 기본 컴포넌트 설정

---

## 12. 최종 결정 사항

### 12.1 결정된 항목

1. **설계 도구**: ✅ **Figma**
   - 협업 및 프로토타입 제작
   - 컴포넌트 시스템 구축

2. **설계 프로세스**: ✅ **프로세스 B (빠른 프로토타이핑)**
   - 핵심 화면 와이어프레임 (3일)
   - 간단한 프로토타입 (3일)
   - 기본 디자인 시스템 (2일)
   - 개발 시작 (동시 진행)
   - 반복적 개선

3. **스타일링 방법**: ✅ **StyleSheet**
   - React Native 기본 StyleSheet 사용
   - Theme 객체로 일관성 유지
   - 다크 모드 지원

4. **디자인 리소스**: ✅ **디자이너 없이 진행**
   - Material Design / Human Interface Guidelines 참고
   - 기존 러닝 앱 벤치마킹
   - 개발 중 지속적 개선

---

## 13. 프로세스 B 실행 계획 (최종)

### 13.1 타임라인

**Week 1: 핵심 설계 (8일)**

**Day 1-2: 사용자 플로우 및 정보 아키텍처**
- [ ] 코스 생성 플로우 다이어그램 작성
- [ ] 러닝 추적 플로우 다이어그램 작성
- [ ] 화면 목록 및 네비게이션 구조 정의
- [ ] 정보 우선순위 정의

**Day 3-5: 핵심 화면 와이어프레임 (Figma)**
- [ ] MapScreen 와이어프레임
- [ ] CourseGenerationScreen 와이어프레임
- [ ] RunningScreen 와이어프레임
- [ ] CourseListScreen 와이어프레임 (간단히)

**Day 6-8: 기본 디자인 시스템 및 프로토타입**
- [ ] 색상 팔레트 정의
- [ ] 타이포그래피 시스템 정의
- [ ] 간격 시스템 정의
- [ ] 핵심 화면 하이파이 프로토타입 (기본 스타일)
- [ ] 기본 인터랙션 정의

**Week 2: 개발 시작 및 병행**

- [ ] React Native 프로젝트 초기화
- [ ] 기본 컴포넌트 구조 생성
- [ ] 디자인 시스템을 코드로 구현 (Theme 객체)
- [ ] 핵심 화면 기본 레이아웃 구현
- [ ] 개발 중 지속적 개선

### 13.2 디자이너 없이 진행하는 방법

#### 13.2.1 참고 자료 활용

**Material Design (Android)**
- 컴포넌트 가이드라인
- 색상 시스템
- 타이포그래피
- 간격 시스템
- URL: https://material.io/design

**Human Interface Guidelines (iOS)**
- iOS 디자인 원칙
- 컴포넌트 가이드라인
- URL: https://developer.apple.com/design/human-interface-guidelines/

**기존 러닝 앱 벤치마킹**
- Strava
- Nike Run Club
- Runkeeper
- MapMyRun

#### 13.2.2 디자인 시스템 구축 전략

**1. 색상 팔레트 (참고 기반)**
```typescript
// theme/colors.ts
export const colors = {
  // Primary: 러닝 앱 특성에 맞는 활기찬 색상
  primary: '#FF6B35',      // 오렌지 (에너지)
  primaryDark: '#E85A2B',
  primaryLight: '#FF8C5A',
  
  // Secondary: 보조 색상
  secondary: '#4ECDC4',     // 청록 (신선함)
  
  // Background
  background: '#FFFFFF',
  surface: '#F5F5F5',
  
  // Text
  text: '#212121',
  textSecondary: '#757575',
  
  // Status
  success: '#4CAF50',
  error: '#F44336',
  warning: '#FF9800',
  
  // 다크 모드
  dark: {
    background: '#121212',
    surface: '#1E1E1E',
    text: '#FFFFFF',
    textSecondary: '#B0B0B0',
  }
};
```

**2. 타이포그래피 (시스템 폰트 활용)**
```typescript
// theme/typography.ts
export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 40,
  },
  h2: {
    fontSize: 24,
    fontWeight: '600' as const,
    lineHeight: 32,
  },
  body: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 24,
  },
  caption: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 20,
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
};
```

**3. 간격 시스템 (8px 그리드)**
```typescript
// theme/spacing.ts
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};
```

#### 13.2.3 Figma 템플릿 활용

**무료 Figma 템플릿:**
- Material Design Kit for Figma
- iOS Design Kit for Figma
- React Native UI Kit

**사용 방법:**
1. 템플릿 다운로드
2. 필요한 컴포넌트 복사
3. 프로젝트에 맞게 수정
4. 일관성 유지

### 13.3 구체적인 실행 단계

#### Step 1: 사용자 플로우 작성 (Day 1-2)

**산출물:**
- 사용자 플로우 다이어그램 (Figma 또는 Miro)
- 화면 목록 문서

**작성 내용:**
1. 코스 생성 플로우
   ```
   MapScreen → 거리 입력 → 코스 생성 요청 → 
   생성 중 표시 → 코스 미리보기 → 저장/사용 선택
   ```

2. 러닝 추적 플로우
   ```
   MapScreen → 코스 선택 → 러닝 시작 → 
   러닝 중 화면 → 일시정지/종료 → 결과 화면
   ```

#### Step 2: 와이어프레임 작성 (Day 3-5)

**Figma에서 작성할 화면:**

1. **MapScreen**
   - 지도 영역 (전체 화면의 70%)
   - 하단 버튼 영역
   - 현재 위치 마커
   - 코스 폴리라인

2. **CourseGenerationScreen**
   - 지도 영역 (60%)
   - 거리 입력 영역
   - 프리셋 버튼
   - 생성 버튼
   - 진행 상태 표시

3. **RunningScreen**
   - 지도 영역 (50%)
   - 통계 표시 영역 (상단 또는 하단)
   - 컨트롤 버튼 (하단)

4. **CourseListScreen**
   - 검색 바
   - 코스 카드 리스트
   - 필터 옵션 (선택사항)

#### Step 3: 기본 디자인 시스템 (Day 6-7)

**Figma에서 작성:**
- 색상 스와치
- 타이포그래피 스타일
- 간격 가이드
- 기본 버튼 스타일
- 입력 필드 스타일

**코드로 구현:**
- `theme/colors.ts`
- `theme/typography.ts`
- `theme/spacing.ts`
- `theme/index.ts` (통합)

#### Step 4: 하이파이 프로토타입 (Day 8)

**Figma에서:**
- 와이어프레임에 실제 색상/폰트 적용
- 기본 인터랙션 연결
- 화면 간 전환 애니메이션 정의

---

## 14. 개발 중 디자인 개선 전략

### 14.1 반복적 개선 원칙

1. **기능 우선, 디자인 후순**
   - 먼저 기능 구현
   - 작동 확인 후 디자인 개선

2. **사용자 피드백 수집**
   - 베타 테스트
   - 실제 사용 시나리오 테스트
   - 피드백 반영

3. **점진적 개선**
   - 한 번에 완벽하게 만들지 않음
   - 지속적 개선

### 14.2 디자인 개선 체크리스트

개발 중 다음을 점검:

- [ ] 색상 대비 (접근성)
- [ ] 버튼 크기 (최소 44x44pt)
- [ ] 폰트 크기 (가독성)
- [ ] 간격 일관성
- [ ] 다크 모드 지원
- [ ] 에러 상태 디자인
- [ ] 로딩 상태 디자인
- [ ] 빈 상태 (Empty State) 디자인

---

## 15. 다음 단계

### 즉시 진행할 작업

1. **사용자 플로우 다이어그램 작성** (Figma 또는 Miro)
2. **핵심 화면 와이어프레임 작성** (Figma)
3. **기본 디자인 시스템 정의** (Figma + 코드)
4. **React Native 프로젝트 초기화 및 Theme 설정**

### 예상 산출물

1. **Figma 파일**
   - 사용자 플로우 다이어그램
   - 와이어프레임 (4개 핵심 화면)
   - 디자인 시스템 (색상, 타이포그래피, 간격)
   - 하이파이 프로토타입

2. **코드 파일**
   - `theme/` 폴더 (색상, 타이포그래피, 간격)
   - 기본 컴포넌트 구조
   - 화면 레이아웃 기본 구조

---

**프로세스 B로 진행하며, 개발과 병행하여 지속적으로 개선합니다.**

