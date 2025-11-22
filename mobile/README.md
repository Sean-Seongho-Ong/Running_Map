# Running Map App - Mobile

React Native (TypeScript) + Expo Bare Workflow 기반 모바일 애플리케이션

## 프로젝트 구조

```
├── src/
│   ├── domain/                    # 비즈니스 로직 (순수 TypeScript)
│   │   ├── entities/              # 도메인 엔티티
│   │   │   ├── Course.ts
│   │   │   └── RunningSession.ts
│   │   └── valueObjects/          # 값 객체
│   │       ├── Coordinate.ts
│   │       └── Distance.ts
│   │
│   ├── application/               # 유즈케이스 및 리포지토리
│   │   └── repositories/          # 리포지토리 구현
│   │       ├── CourseRepository.ts
│   │       └── RunningRepository.ts
│   │
│   ├── infrastructure/            # 인프라 계층
│   │   └── api/                   # API 클라이언트
│   │       ├── client.ts          # Axios 인스턴스
│   │       ├── endpoints.ts       # API 엔드포인트 상수
│   │       └── types.ts           # API 타입 정의
│   │
│   ├── interface/                 # UI 계층
│   │   ├── components/            # 컴포넌트
│   │   │   ├── common/            # 공통 컴포넌트
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   └── Loading.tsx
│   │   │   ├── map/               # 지도 컴포넌트
│   │   │   │   ├── MapView.tsx
│   │   │   │   ├── CoursePolyline.tsx
│   │   │   │   └── LocationMarker.tsx
│   │   │   └── running/           # 러닝 컴포넌트
│   │   │       ├── RunningStats.tsx
│   │   │       ├── PaceDisplay.tsx
│   │   │       └── ElevationDisplay.tsx
│   │   ├── screens/               # 화면
│   │   │   ├── MapScreen.tsx
│   │   │   ├── CourseGenerationScreen.tsx
│   │   │   ├── RunningScreen.tsx
│   │   │   └── CourseListScreen.tsx
│   │   ├── navigation/            # 네비게이션
│   │   │   └── AppNavigator.tsx
│   │   ├── hooks/                 # 커스텀 훅
│   │   │   └── useTheme.ts
│   │   └── store/                 # Zustand 스토어
│   │       ├── courseStore.ts
│   │       ├── runningStore.ts
│   │       └── locationStore.ts
│   │
│   ├── theme/                     # 디자인 시스템
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   ├── spacing.ts
│   │   └── index.ts
│   │
│   └── config.ts                  # 환경 설정 (API URL 등)
│
├── cursor-talk-to-figma-mcp/      # Figma MCP 통합 도구
│   ├── src/
│   │   ├── talk_to_figma_mcp/     # MCP 서버
│   │   ├── cursor_mcp_plugin/     # Figma 플러그인
│   │   └── socket.ts              # WebSocket 서버
│   └── readme.md                  # Figma MCP 사용 가이드
│
├── App.tsx                         # 앱 진입점
├── package.json                    # 의존성 관리
├── Front_todo.md                   # 프론트엔드 작업 체크리스트
└── node_modules/                   # 설치된 패키지
```

**참고**: 
- `ios/` 및 `android/` 폴더는 `expo run:ios` 또는 `expo run:android` 실행 시 자동 생성됩니다.

## 설치 및 실행

### 1. 의존성 설치

```bash
npm install
```

또는 Bun을 사용하는 경우:

```bash
bun install
```

### 2. iOS 의존성 설치 (macOS만)

```bash
cd ios && pod install && cd ..
```

### 3. 개발 서버 시작

```bash
# 개발 서버 시작
npm start

# 또는 직접 실행
npm run android  # Android
npm run ios      # iOS (macOS만)
```

### 4. Expo Dev Client

프로젝트는 Expo Bare Workflow를 사용하므로, 개발 중에는 Expo Dev Client를 통해 디버깅할 수 있습니다.

```bash
# Expo Dev Client 설치 (이미 package.json에 포함됨)
npx expo install expo-dev-client

# 개발 빌드 생성
npx expo run:android
# 또는
npx expo run:ios
```

## Figma MCP 연동 (디자인 작업)

이 프로젝트는 **Figma MCP (Model Context Protocol)**를 사용하여 디자인 작업을 수행합니다. Cursor AI를 통해 Figma와 직접 통신하여 디자인을 읽고 수정할 수 있습니다.

### 사전 요구사항

1. **Bun 설치** (이미 설치되어 있음)
   ```bash
   # Windows
   powershell -c "irm bun.sh/install.ps1|iex"
   ```

2. **Figma Desktop 앱** 설치
   - [Figma Desktop 다운로드](https://www.figma.com/downloads/)

3. **Figma Plugin 설치**
   - Figma Community에서 [Cursor Talk to Figma MCP Plugin](https://www.figma.com/community/plugin/1485687494525374295/cursor-talk-to-figma-mcp-plugin) 설치
   - 또는 로컬 플러그인 사용: `mobile/cursor-talk-to-figma-mcp/` 참고

### Figma MCP 설정

1. **WebSocket 서버 시작**

   ```bash
   cd mobile/cursor-talk-to-figma-mcp
   bun socket
   ```

   Windows + WSL 사용 시 `src/socket.ts`에서 `hostname: "0.0.0.0"` 주석 해제 필요

2. **Figma에서 플러그인 실행**
   - Figma Desktop 앱 열기
   - Plugins > Development > Cursor Talk to Figma MCP Plugin 실행
   - 채널 연결 (예: `join_channel` 명령으로 채널 이름 설정)

3. **Cursor에서 Figma 작업**
   - Cursor AI를 통해 Figma 디자인 읽기/수정
   - 예: "원을 그려줘", "색상을 변경해줘" 등

### Figma MCP 주요 기능

- **디자인 읽기**: 문서 정보, 선택된 요소 정보 조회
- **요소 생성**: 프레임, 사각형, 텍스트 등 생성
- **스타일 수정**: 색상, 크기, 위치, corner radius 등 변경
- **Auto Layout 설정**: 레이아웃 모드, 패딩, 정렬 설정
- **컴포넌트 관리**: 컴포넌트 인스턴스 생성 및 오버라이드
- **주석 관리**: Figma 네이티브 주석 생성 및 관리

### 디자인 작업 워크플로우

1. Figma에서 디자인 파일 열기
2. WebSocket 서버 실행 (`bun socket`)
3. Figma 플러그인에서 채널 연결
4. Cursor AI를 통해 디자인 작업 수행
5. 실시간으로 Figma에 반영 확인

자세한 사용법은 `mobile/cursor-talk-to-figma-mcp/readme.md` 참고.

## 주요 기능

- 🗺️ **지도 표시**: OSM 타일을 사용한 지도 표시
- 📍 **코스 생성**: 거리 제약 루프 생성 알고리즘
- 🏃 **러닝 추적**: 실시간 속도, 페이스, 고저차 측정
- 💾 **코스 저장 및 로드**: 로컬 저장 및 백엔드 동기화

## 기술 스택

- **프레임워크**: React Native (TypeScript) + Expo Bare Workflow
- **지도**: react-native-maps (OSM 타일)
- **네비게이션**: @react-navigation (Bottom Tab + Stack)
- **상태 관리**: Zustand
- **위치 서비스**: @react-native-community/geolocation
- **HTTP 클라이언트**: Axios
- **스타일링**: StyleSheet
- **스토리지**: @react-native-async-storage/async-storage
- **디자인 도구**: Figma MCP (Model Context Protocol)
- **패키지 매니저**: npm 또는 Bun

## 개발 가이드

### Clean Architecture 원칙

프로젝트는 Clean Architecture 원칙을 따라 구성됩니다:

- **Domain**: 순수 비즈니스 로직, 외부 의존성 없음 (구현 완료)
  - 엔티티: Course, RunningSession
  - 값 객체: Coordinate, Distance
- **Application**: 유즈케이스 및 리포지토리 (구현 완료)
  - 리포지토리: CourseRepository, RunningRepository
  - 유즈케이스: 향후 구현 예정
- **Infrastructure**: API 클라이언트, 스토리지 구현 (구현 완료)
  - API Client: Axios 기반 HTTP 클라이언트
  - API Types: TypeScript 타입 정의
  - API Endpoints: 엔드포인트 상수
- **Interface**: UI 컴포넌트, 네비게이션, 상태 관리 (구현 완료)
  - 컴포넌트: 공통, 지도, 러닝 컴포넌트
  - 화면: MapScreen, CourseGenerationScreen, RunningScreen, CourseListScreen
  - 상태 관리: Zustand 스토어 (courseStore, runningStore, locationStore)
  - API 연동: Repository 패턴을 통한 백엔드 통신

### 코딩 규칙

- SOLID 원칙 준수
- TypeScript 타입 안정성
- 함수형 컴포넌트 + Hooks
- 컴포넌트 재사용성 강조

### 주요 컴포넌트

#### 공통 컴포넌트
- `Button`: 재사용 가능한 버튼
- `Input`: 텍스트 입력 필드
- `Card`: 카드 컨테이너
- `Loading`: 로딩 인디케이터

#### 지도 컴포넌트
- `MapView`: 지도 뷰 (OSM 타일)
- `CoursePolyline`: 코스 폴리라인
- `LocationMarker`: 사용자 위치 마커

#### 러닝 컴포넌트
- `RunningStats`: 러닝 통계 표시
- `PaceDisplay`: 페이스 표시
- `ElevationDisplay`: 고저차 표시

### 상태 관리

Zustand를 사용한 전역 상태 관리:

- `courseStore`: 코스 관련 상태
- `runningStore`: 러닝 세션 상태
- `locationStore`: 위치 정보

### 네비게이션 구조

Bottom Tab Navigator + Stack Navigator:

- **Map Tab**: 지도 화면
- **Courses Tab**: 코스 목록 화면
- **Running Tab**: 러닝 화면
- **Profile Tab**: 프로필 화면 (향후)

## 테스트

```bash
# 타입 체크
npm run type-check

# 린트
npm run lint
```

## 빌드

### Android

```bash
npm run android
```

### iOS

```bash
npm run ios
```

## 환경 변수

백엔드 API URL 설정:

```typescript
// src/infrastructure/config/api.ts
export const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000' 
  : 'https://api.runningmap.com';
```

## 문제 해결

### 일반적인 문제

1. **iOS 빌드 실패**
   ```bash
   cd ios && pod install && cd ..
   ```

2. **Android 빌드 실패**
   - Android Studio에서 프로젝트 열기
   - Gradle 동기화

3. **지도가 표시되지 않음**
   - `ios/Info.plist` 및 `android/AndroidManifest.xml`에서 위치 권한 확인
   - TileServer GL 서버가 실행 중인지 확인

4. **의존성 오류**
   ```bash
   rm -rf node_modules
   npm install
   ```

5. **Expo 캐시 문제**
   ```bash
   expo start -c
   ```

## 현재 상태 (2025-11-22)

### 완료된 작업 ✅
- ✅ API 통합 완료 (Axios 클라이언트, Repository 패턴, Zustand 연동)
- ✅ UI Integration 부분 완료
  - ✅ CourseGenerationScreen 연동 (API 호출, 로딩, 에러 처리, 상세 정보 표시)
  - ✅ MapScreen 연동 (생성된 코스 표시, 네비게이션, 지도 제어)
  - ✅ 코스 재생성 기능
  - ✅ UX 개선 (네비게이션 흐름 수정)
- ✅ TypeScript 오류 수정 완료
- ✅ Android 빌드 성공 (compileSdkVersion 34)

### 현재 문제 ⚠️
- ⚠️ **앱 로드 실패**: Android Studio에서 빌드는 성공했지만 앱이 JavaScript 번들을 로드하지 못함
  - Metro Bundler는 정상 실행 중
  - WebSocket 연결 오류 발생
  - Expo Dev Client에서 서버 선택 후 로드되지 않음

## 다음 단계

1. **프론트엔드 앱 로드 문제 해결** (우선순위 높음)
   - Metro Bundler 연결 문제 해결
   - Expo Dev Client 방식으로 앱 정상 실행 확인
   - WebSocket 연결 문제 해결

2. **러닝 추적 기능 구현**
   - GPS 위치 추적
   - 실시간 통계 계산
   - 백엔드 동기화 (이미 구현됨)

3. **코스 관리 기능 완성**
   - 코스 목록 화면 API 연동
   - 코스 검색 기능
   - 코스 저장/로드 기능

4. **코스 생성 알고리즘 구현** (백엔드)
   - DistanceConstrainedLoopGenerator 구현

5. **디자인 작업** (Figma MCP 활용)
   - 화면별 하이파이 디자인 완성
   - 컴포넌트 디자인 시스템 구축
   - 인터랙션 프로토타입 작성

## API 명세서

백엔드 API 명세서는 `../plan/api-specification.yaml`에 정의되어 있습니다.

- **OpenAPI 3.0 형식**: 모든 엔드포인트, 요청/응답 스키마 포함
- **Mock 서버 생성 가능**: API 명세서를 기반으로 Mock 서버 생성하여 프론트엔드 개발 가능
- **타입 안정성**: API 스펙을 기반으로 TypeScript 타입 생성 가능

자세한 내용은 `../plan/api-specification.yaml`, `../plan/SDS_Running_App.md` 및 `plan/Frontend_Architecture_Design.md` 참고.

