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

### Android 에뮬레이터 시작

#### 방법 1: Android Studio에서 직접 시작 (권장)

1. **Android Studio 열기**
   - 프로젝트 열기: `C:\Running_map\mobile\android` 폴더

2. **에뮬레이터 시작**
   - **Tools** → **Device Manager** 클릭
   - 에뮬레이터가 있으면 ▶️ (Play) 버튼 클릭
   - 없으면 **Create Device** 버튼 클릭하여 생성

3. **에뮬레이터 생성 (필요시)**
   - **Phone** 카테고리 선택
   - 추천 기기 선택 (예: Pixel 5, Pixel 6)
   - 시스템 이미지 선택 (API Level 33 이상 권장)
   - **Finish** 클릭

4. **확인**
   ```powershell
   adb devices
   ```
   `device`가 표시되면 정상입니다.

#### 문제 해결

- **에뮬레이터가 시작되지 않음**: BIOS에서 가상화 기능 활성화 확인
- **에뮬레이터가 느림**: Graphics를 **Hardware - GLES 2.0**으로 설정

### Android Studio Terminal에서 ADB 사용

Android Studio 터미널에서 `adb` 명령어가 인식되지 않는 경우:

#### 빠른 해결책

```powershell
# 1. ADB 경로 찾기
cd mobile
.\scripts\find_adb.ps1

# 2. 출력된 경로를 사용하여 PATH에 추가 (예시)
$env:Path += ";C:\Users\User\AppData\Local\Android\Sdk\platform-tools"

# 3. 확인
adb devices

# 4. 포트 포워딩 설정
adb reverse tcp:8081 tcp:8081
```

#### 영구적으로 PATH에 추가

1. Windows 검색: "환경 변수"
2. "시스템 환경 변수 편집" 선택
3. "환경 변수" → "시스템 변수" → `Path` 편집
4. 다음 경로 추가:
   ```
   C:\Users\User\AppData\Local\Android\Sdk\platform-tools
   ```
5. 새 터미널 창 열기

#### 자동화 스크립트 사용

```powershell
cd mobile
.\scripts\setup_metro_connection.ps1
```

### Metro Bundler 연결 설정

Android Studio에서 앱을 실행하기 전에 Metro Bundler와의 연결을 설정합니다.

#### 빠른 시작

1. **포트 포워딩 설정**
   ```powershell
   cd mobile
   .\scripts\setup_metro_connection.ps1
   ```

2. **Metro Bundler 시작 (캐시 클리어)**
   ```powershell
   cd mobile
   .\scripts\start_metro_clean.ps1
   ```

3. **Android Studio에서 앱 실행**
   - Android Studio에서 앱 빌드 및 실행
   - Expo Dev Client 화면에서 서버 선택

#### 수동 설정

1. **포트 포워딩**
   ```bash
   adb reverse tcp:8081 tcp:8081
   adb reverse --list  # 확인
   ```

2. **Metro Bundler 시작**
   ```bash
   cd mobile
   npm start
   # 또는
   expo start --dev-client --clear
   ```

3. **확인 사항**
   - Metro Bundler: `Metro waiting on exp://192.168.x.x:8081` 메시지 확인
   - 포트 포워딩: `adb reverse --list`에서 `8081 tcp:8081` 확인

#### 문제 해결

- **포트 8081이 이미 사용 중**: `netstat -ano | findstr :8081`로 프로세스 확인 후 종료
- **WebSocket 연결 오류**: 캐시 클리어 후 재시작, 방화벽 포트 8081 허용
- **앱이 번들을 로드하지 못함**: Android Studio에서 Clean & Rebuild, 앱 재시작

### Expo Dev Client 연결 오류

#### 오류 메시지
```
DevLauncher E Unable to inject debug server host settings.
java.lang.NoSuchFieldException: No field mPackagerConnectionSettings
```

#### 해결 방법

**방법 1: Clean & Rebuild (권장)**
1. Android Studio: **Build** → **Clean Project**
2. **Build** → **Rebuild Project**
3. 앱 재실행

**방법 2: Expo Dev Client 재설치**
```powershell
cd mobile
npx expo install expo-dev-client
cd android
.\gradlew clean
cd ..
npx expo run:android
```

**방법 3: 완전한 재설정**
```powershell
cd mobile
Remove-Item -Recurse -Force node_modules\.cache, .expo, .metro, android\app\build, android\.gradle -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force node_modules
npm install
```
Android Studio에서 **Build** → **Clean Project** → **Rebuild Project**

### Gradle 캐시 오류

#### 오류 메시지
```
Unable to load class 'org.gradle.api.artifacts.SelfResolvingDependency'
Gradle's dependency cache may be corrupt
```

#### 해결 방법

**방법 1: Gradle 캐시 삭제 (권장)**
```powershell
cd mobile\android
.\gradlew --stop
Remove-Item -Recurse -Force .gradle, app\build, build -ErrorAction SilentlyContinue
```
Android Studio에서 **File** → **Sync Project with Gradle Files**

**방법 2: 사용자 Gradle 캐시 삭제**
```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.gradle\caches -ErrorAction SilentlyContinue
```

**방법 3: 완전한 재설정**
1. Android Studio 완전히 종료
2. 모든 Gradle 관련 파일 삭제 (위 명령 실행)
3. Android Studio 재시작
4. **File** → **Invalidate Caches...** → **Invalidate and Restart**

#### 빠른 해결 스크립트
```powershell
cd mobile\android
.\gradlew --stop
Remove-Item -Recurse -Force .gradle, app\build, build -ErrorAction SilentlyContinue
Write-Host "Done! Now sync the project in Android Studio." -ForegroundColor Green
```

### 버전 정보

#### 현재 버전 설정
- **Gradle**: 7.5.1
- **Android Gradle Plugin**: 7.4.2
- **compileSdkVersion**: 33
- **targetSdkVersion**: 33
- **buildToolsVersion**: 33.0.0
- **Kotlin**: 1.8.22
- **minSdkVersion**: 21

#### 버전 업데이트 이력
- Gradle: 7.6.3 → 7.5.1
- compileSdkVersion: 34 → 33
- buildToolsVersion: 34.0.0 → 33.0.0
- Kotlin: 1.8.10 → 1.8.22

### 빠른 시작 가이드

#### 현재 상태 확인
```powershell
# 포트 포워딩 확인
adb reverse --list
# host-20 tcp:8081 tcp:8081 이 보여야 함
```

#### 다음 단계

1. **Metro Bundler 시작**
   ```powershell
   cd C:\Running_map\mobile
   npm start
   ```
   또는 캐시 클리어 후:
   ```powershell
   .\scripts\start_metro_clean.ps1
   ```

2. **Android Studio에서 앱 실행**
   - Android Studio 열기
   - 에뮬레이터 확인 (Device Manager)
   - ▶️ (Run) 버튼 클릭

3. **Expo Dev Client에서 서버 선택**
   - 앱 시작 후 Expo Dev Client 화면에서 서버 선택
   - JavaScript 번들 로드 확인

#### 성공 확인
- ✅ 첫 화면 (MapScreen) 표시
- ✅ 개발자 메뉴 접근 가능 (`Ctrl + M`)
- ✅ Metro Bundler 터미널에 번들 요청 로그 표시

## 현재 상태 (2025-11-22)

### 완료된 작업 ✅
- ✅ API 통합 완료 (Axios 클라이언트, Repository 패턴, Zustand 연동)
  - ✅ CourseRepository 구현 완료
  - ✅ RunningRepository 구현 완료 (백엔드 응답 형식에 맞게 수정 완료)
  - ✅ API 타입 정의 완료 (백엔드 DTO와 일치)
  - ✅ 로깅 규칙 준수 (Logger 유틸리티 사용)
- ✅ UI Integration 부분 완료
  - ✅ CourseGenerationScreen 연동 (API 호출, 로딩, 에러 처리, 상세 정보 표시)
  - ✅ MapScreen 연동 (생성된 코스 표시, 네비게이션, 지도 제어)
  - ✅ 코스 재생성 기능
  - ✅ UX 개선 (네비게이션 흐름 수정)
- ✅ TypeScript 오류 수정 완료
- ✅ Android 빌드 성공
  - ✅ 빌드 환경 설정 완료
    - Java 17 설정 (gradle.properties: `org.gradle.java.home=C:\\Users\\User\\.jdks\\temurin-17.0.17`)
    - Gradle 7.5.1 유지 (Java 17 호환)
    - compileSdkVersion 33 유지
  - ✅ 의존성 버전 호환성 조정 완료
    - androidx.appcompat: 1.7.0 → 1.6.1 (compileSdk 33 호환)
    - androidx.core: 1.16.0 → 1.10.1 (compileSdk 33 호환)
    - androidx.annotation-experimental: 1.4.1 → 1.3.1 (compileSdk 33 호환)
    - build.gradle에 resolutionStrategy 추가
  - ✅ react-native-gesture-handler 버전 조정 완료 (2.29.1 → 2.12.0)
  - ✅ NullPointerException 해결 완료
    - build.gradle의 packagingOptions 루프 null 체크 강화
    - entryFile 설정 null 체크 강화
  - ✅ Gradle 빌드 성공 (assembleDebug 완료, APK 생성 성공)
- ⚠️ 다음 단계: 에뮬레이터에 앱 설치 및 실행
- ✅ **Figma 화면 구성 디자인 완료** (채널: ra1r3dhi)
  - ✅ MapScreen (지도 메인 화면)
  - ✅ CourseGenerationScreen (코스 생성 화면)
  - ✅ CourseListScreen (코스 목록 화면)
  - ✅ RunningScreen (러닝 추적 화면)
- ✅ **Figma 디자인 코드 적용 완료**
  - ✅ Theme 색상 추가 (surfaceLight #fafafa, mapBackground #d9d9d9, borderGray #e0e0e0)
  - ✅ Button 컴포넌트 스타일 수정 (outline variant 흰색 배경/회색 테두리, 높이 조정)
  - ✅ Card 컴포넌트 스타일 수정 (모서리 8px, 테두리 추가)
  - ✅ MapScreen 스타일 수정 (Map Area 여백, Button Container 패딩)
  - ✅ CourseGenerationScreen 스타일 수정 (Input Container 배경색, Preset 버튼 크기)
  - ✅ CourseListScreen 스타일 수정 (Search Container 높이, 카드 크기)
  - ✅ RunningScreen 스타일 수정 (Stats Container, Control Container 패딩)

### 다음 단계
- ⚠️ **에뮬레이터에 앱 설치 및 실행**: Android Studio에서 빌드는 성공했고 APK가 생성됨
  - APK 위치: `mobile/android/app/build/outputs/apk/debug/`
  - Android Studio에서 에뮬레이터 실행 후 앱 설치 필요
  - 또는 `adb install` 명령으로 직접 설치 가능

## 개발 전략: Android Studio vs Expo Go

### 권장 방식: Android Studio + Expo Dev Client 유지 ✅

**이유:**
1. **네이티브 모듈 필수**: `react-native-maps`, `@react-native-community/geolocation` 사용 중
2. **빌드 성공**: Android Studio 빌드 완료, APK 생성 성공
3. **코드 변경 최소화**: 현재 구현된 코드를 그대로 사용 가능
4. **프로덕션 준비**: 실제 배포 환경과 동일한 구조

**Expo Go로 전환 시 문제점:**
- ❌ `react-native-maps` 미지원 → 대규모 코드 수정 필요
- ❌ `@react-native-community/geolocation` 미지원 → 위치 추적 로직 재작성 필요
- ❌ 프로덕션 배포 불가

### Metro Bundler 연결 문제 해결 방법

1. **캐시 클리어 후 재시작**
   ```bash
   cd mobile
   expo start -c --dev-client
   ```

2. **네트워크 설정 확인**
   - 방화벽에서 포트 8081 허용
   - `adb reverse tcp:8081 tcp:8081` 포트 포워딩
   - WebSocket 연결 테스트

3. **대안 방법**
   - `npx react-native start` 직접 실행
   - 물리 기기 사용 (에뮬레이터 대신)

## 다음 단계

### 우선순위 1: 프론트엔드 앱 로드 문제 해결 (즉시 필요)
1. **Metro Bundler 연결 문제 해결**
   - **결정**: Android Studio + Expo Dev Client 유지 (네이티브 모듈 필수)
   - **해결 방법**:
     - 캐시 클리어: `expo start -c --dev-client`
     - 네트워크 설정 확인: 방화벽 포트 8081 허용
     - 포트 포워딩: `adb reverse tcp:8081 tcp:8081`
     - WebSocket 연결 테스트
   - **목표**: 앱이 정상적으로 JavaScript 번들을 로드하고 실행됨

### 우선순위 2: 앱 기능 테스트 (앱 로드 후)
2. **UI/UX 검증**
   - Figma 디자인 적용 확인 (레이아웃, 색상, 크기)
   - 네비게이션 흐름 검증
   - 로딩 상태 표시 확인
   - 에러 처리 확인
3. **API 통합 테스트**
   - 코스 목록 조회 테스트 (샘플 데이터 9개 확인)
   - 코스 생성 테스트 (MockLoopGenerator 검증)
   - 코스 상세 정보 표시 확인
   - Running API 통합 테스트 (시작, 위치 업데이트, 종료)

### 우선순위 3: 러닝 추적 기능 구현
4. **GPS 위치 추적 구현**
   - 위치 권한 요청
   - GPS 위치 추적 시작/중지
   - 주기적 위치 업데이트 (예: 5초마다)
   - 위치 정확도 필터링
5. **실시간 통계 계산**
   - 거리 계산 (Haversine 공식)
   - 시간 계산
   - 페이스 계산 (분/km)
   - 속도 계산 (km/h)
   - 고저차 계산 (가속도계/기압계 활용)
6. **RunningScreen 완전 연동**
   - GPS 추적과 UI 연동
   - 실시간 통계 표시
   - 러닝 경로 지도 표시
   - 백엔드 동기화 (이미 구현됨)

### 우선순위 4: 코스 관리 기능 완성
7. **코스 목록 화면 API 연동**
   - 코스 목록 조회 API 호출
   - 코스 카드 클릭 시 상세 정보 표시
   - 코스 삭제 기능
8. **코스 검색 기능**
   - 실시간 검색 필터링 (이미 구현됨)
   - 검색 결과 표시
9. **코스 저장 기능**
   - 생성된 코스 저장 API 호출
   - 저장 성공/실패 처리

### 우선순위 5: 코스 생성 알고리즘 구현 (백엔드)
10. **DistanceConstrainedLoopGenerator 구현**
    - Step 기반 원둘레 분할
    - 양방향 Adaptive Step 피드백
    - S-P 기반 Fallback
    - 도로 스냅핑 로직
    - 루프 폐쇄 검증
    - 자가 교차 검증
    - 알고리즘 단위 테스트 작성

**최근 업데이트 (2025-11-22)**:
- ✅ Figma 디자인 코드 적용 완료 (모든 화면의 레이아웃, 색상, 크기 반영)
- ✅ Figma 화면 구성 디자인 완료 (4개 주요 화면)
- ✅ 프론트엔드 API 코드 검토 및 수정 완료
  - RunningRepository 응답 처리 수정 (백엔드 응답 형식에 맞게)
  - API 타입 정의 추가 및 수정
  - 로깅 규칙 준수 (Logger 유틸리티 사용)

## API 명세서

백엔드 API 명세서는 `../plan/api-specification.yaml`에 정의되어 있습니다.

- **OpenAPI 3.0 형식**: 모든 엔드포인트, 요청/응답 스키마 포함
- **Mock 서버 생성 가능**: API 명세서를 기반으로 Mock 서버 생성하여 프론트엔드 개발 가능
- **타입 안정성**: API 스펙을 기반으로 TypeScript 타입 생성 가능

자세한 내용은 `../plan/api-specification.yaml`, `../plan/SDS_Running_App.md` 및 `plan/Frontend_Architecture_Design.md` 참고.

---

## 주요 화면 요구 명세서

이 섹션은 Running Map App의 4개 주요 화면에 대한 상세 요구 명세서입니다. 화면 구조, 레이아웃, 기능, 네비게이션 흐름을 포함합니다.

### 화면 개요

앱은 4개의 주요 화면으로 구성됩니다:
1. **MapScreen**: 지도 메인 화면
2. **CourseGenerationScreen**: 코스 생성 화면
3. **CourseListScreen**: 코스 목록 화면
4. **RunningScreen**: 러닝 추적 화면

**화면 크기**: 모든 화면은 375x812 (iPhone 기준) 크기로 설계됨

---

### 1. MapScreen (지도 메인 화면)

#### 화면 목적
- 현재 위치를 지도에 표시
- 생성된 코스를 지도에 표시
- 코스 생성 및 내 코스 목록으로 이동

#### 레이아웃 구조

**Container (전체 화면)**
- 타입: `View`
- 스타일: `flex: 1`
- 배경색: `theme.colors.background`

**Map Area (지도 영역)**
- 타입: `CustomMapView`
- 위치: (10, 11) - 상단 여백 10px, 좌측 여백 10px
- 크기: 355x483
- 스타일: `flex: 1`
- 배경색: 회색 (#d9d9d9)
- 기능:
  - 현재 위치 표시
  - 생성된 코스 폴리라인 표시 (있는 경우)
  - 현재 위치 버튼 표시 (`showLocationButton={true}`)

**Button Container (버튼 컨테이너)**
- 타입: `View`
- 위치: (0, 483) - Map Area 아래
- 크기: 375x132
- 배경색: 흰색
- 스타일:
  - 패딩: `theme.spacing.md` (16px)
  - 배경색: `theme.colors.surface`
  - gap: `theme.spacing.sm`

#### 버튼 명세

**"코스 생성" 버튼**
- 타입: `Button`
- 위치: (16, 499)
- 크기: 343x48
- variant: `primary` (주요 버튼, 주황색 RGB: 1, 0.42, 0.21)
- fullWidth: `true`
- 텍스트: "코스 생성" (흰색, 16px, Semi Bold)
- 텍스트 위치: (156, 513) - 버튼 중앙 정렬
- 모서리: 8px 둥글게
- 기능: `CourseGenerationScreen`으로 이동
- 핸들러: `handleGenerateCourse()`

**"내 코스" 버튼**
- 타입: `Button`
- 위치: (16, 563)
- 크기: 343x48
- variant: `outline` (아웃라인 버튼)
- fullWidth: `true`
- 배경색: 흰색 + 회색 테두리 (RGB: 0.88, 0.88, 0.88, 두께: 1px)
- 텍스트: "내 코스" (검은색, 16px, Semi Bold)
- 텍스트 위치: (163, 577) - 버튼 중앙 정렬
- 모서리: 8px 둥글게
- 기능: `CoursesTab` (CourseListScreen)으로 이동
- 핸들러: `handleViewCourses()`

**버튼 간격**: 64px (563 - 499)

---

### 2. CourseGenerationScreen (코스 생성 화면)

#### 화면 목적
- 목표 거리를 입력받아 코스 생성
- 생성된 코스의 상세 정보 표시
- 생성된 코스 사용 또는 재생성

#### 레이아웃 구조

**Container (전체 화면)**
- 타입: `View`
- 스타일: `flex: 1`
- 배경색: `theme.colors.background`

**Map Area (지도 영역)**
- 타입: `CustomMapView`
- 위치: (11, 10) - 상단 여백 10px, 좌측 여백 10px
- 크기: 355x487 (전체의 60%)
- 스타일: `flex: 0.6`
- 배경색: 회색 (#d9d9d9)
- 기능:
  - 현재 위치 표시
  - 생성된 코스 폴리라인 표시 (생성 후)

**Input Container (입력 컨테이너)**
- 타입: `View`
- 위치: (0, 498) - Map Area 아래
- 크기: 375x325 (전체의 40%)
- 스타일: `flex: 0.4`
- 배경색: 연한 회색 (#fafafa)
- 패딩: 16px
- 내부 구조: `ScrollView` 포함

#### 상태별 UI 구성

**상태 1: 코스 생성 전**

**Input (거리 입력 필드)**
- 타입: `Input`
- 위치: (16, 16)
- 크기: 343x48
- label: "목표 거리 (km)"
- placeholder: "예: 5.0"
- keyboardType: `decimal-pad`
- 배경색: 흰색
- 테두리: 회색
- 기능: 거리 입력 및 에러 메시지 표시

**Preset Container (프리셋 버튼 컨테이너)**
- 타입: `View`
- 위치: (16, 80)
- 스타일:
  - flexDirection: `row`
  - gap: `theme.spacing.sm`
  - marginBottom: `theme.spacing.md`

**프리셋 버튼들** (각 107x40, 3개 가로 배치):
- **"3km" 버튼**
  - variant: `outline`
  - size: `small`
  - flex: `1`
  - 기능: 거리 입력 필드에 "3" 입력

- **"5km" 버튼**
  - variant: `outline`
  - size: `small`
  - flex: `1`
  - 기능: 거리 입력 필드에 "5" 입력

- **"10km" 버튼**
  - variant: `outline`
  - size: `small`
  - flex: `1`
  - 기능: 거리 입력 필드에 "10" 입력

**"코스 생성" 버튼 또는 Loading**
- 위치: (16, 136)
- 크기: 343x48
- 버튼:
  - variant: `primary`
  - fullWidth: `true`
  - disabled: `!distance` (거리 입력 없으면 비활성화)
  - 배경색: 주황색 (#FF6B35)
  - 기능: 코스 생성 API 호출
- Loading (생성 중일 때):
  - 메시지: "코스를 생성하는 중..."

**상태 2: 코스 생성 후**

**CourseDetailInfo (코스 상세 정보 컴포넌트)**
- 타입: `CourseDetailInfo`
- 표시 정보:
  - 목표 거리 (km)
  - 실제 거리 (km)
  - 상대 오차 (%)
  - 알고리즘 이름
  - 반복 횟수
  - 스텝 사용량
  - 상태

**Button Group (버튼 그룹)**
- 타입: `View`
- 스타일:
  - marginTop: `theme.spacing.md`
  - gap: `theme.spacing.sm`

**버튼들:**
- **"이 코스 사용" 버튼**
  - variant: `primary`
  - fullWidth: `true`
  - 기능: MapTab으로 이동하여 생성된 코스 표시
  - 핸들러: `handleUseCourse()`

- **"다시 생성" 버튼**
  - variant: `outline`
  - fullWidth: `true`
  - disabled: `isGenerating`
  - 기능: 동일한 거리로 코스 재생성
  - 핸들러: `handleRegenerate()`

---

### 3. CourseListScreen (코스 목록 화면)

#### 화면 목적
- 저장된 코스 목록 표시
- 코스 검색 기능
- 코스 선택 및 상세 정보 확인

#### 레이아웃 구조

**Container (전체 화면)**
- 타입: `View`
- 스타일: `flex: 1`
- 배경색: `theme.colors.background`

**Search Container (검색 컨테이너)**
- 타입: `View`
- 위치: (0, 0) - 상단 고정
- 크기: 375x80
- 배경색: 연한 회색 (#fafafa)
- 스타일:
  - 패딩: `theme.spacing.md`

**Input (검색 입력 필드)**
- 타입: `Input`
- 위치: (16, 16)
- 크기: 343x48
- placeholder: "코스 검색..." (26, 30), 회색 텍스트
- 배경색: 흰색
- 테두리: 회색
- 모서리: 8px 둥글게
- 기능: 실시간 검색 필터링 (코스 이름 기준)

**List Container (목록 컨테이너)**
- 타입: `View` 또는 `FlatList`
- 위치: (0, 80) - Search Container 아래
- 크기: 375x732
- 배경색: 흰색

**Empty Container (코스가 없을 때)**
- 타입: `View`
- 스타일:
  - flex: `1`
  - justifyContent: `center`
  - alignItems: `center`
- 내용: "저장된 코스가 없습니다." 텍스트

**FlatList (코스가 있을 때)**
- 타입: `FlatList`
- 스타일:
  - contentContainerStyle: `listContainer` (패딩: `theme.spacing.md`)

**코스 카드들**
- 타입: `Card`
- 크기: 343x120
- 카드 간격: 16px
- 카드 위치:
  - 카드 1: (16, 16)
  - 카드 2: (16, 152)
  - 카드 3: (16, 288)
- 카드 스타일:
  - elevated: `true`
  - 배경색: 흰색
  - 테두리: 회색
  - 모서리: 8px 둥글게
  - marginBottom: `theme.spacing.md`

**각 카드 내부 정보:**
- **코스 이름**
  - 스타일: `theme.typography.h3` (20px, Semi Bold)
  - 색상: `theme.colors.text` (검은색)
  - 예시: "서울 한강공원 5km"

- **거리**
  - 스타일: `theme.typography.body` (16px, Regular)
  - 색상: `theme.colors.textSecondary` (회색)
  - 형식: "거리: X.XX km"

- **생성일**
  - 스타일: `theme.typography.caption` (12px, Regular)
  - 색상: `theme.colors.textSecondary` (회색)
  - 형식: "생성일: YYYY-MM-DD"

**카드 기능:**
- 클릭 시: 코스 선택 및 상세 정보 확인 (TODO: 상세 화면으로 이동)

---

### 4. RunningScreen (러닝 추적 화면)

#### 화면 목적
- 러닝 중 실시간 통계 표시
- 러닝 경로 지도 표시
- 러닝 일시정지/재개 및 종료

#### 레이아웃 구조

**Container (전체 화면)**
- 타입: `View`
- 스타일: `flex: 1`
- 배경색: `theme.colors.background`

**Stats Container (통계 컨테이너)**
- 타입: `View`
- 위치: 화면 상단 고정
- 스타일:
  - 패딩: `theme.spacing.md`
  - 배경색: `theme.colors.surface`

**RunningStats 컴포넌트**
- 타입: `RunningStats`
- 구조: 3개의 Row로 구성

**Row 1 (거리, 시간)**
- **거리 (km)**
  - 큰 숫자 표시
  - 형식: "X.XX"
  - 단위: "거리 (km)"

- **시간**
  - 큰 숫자 표시
  - 형식: "HH:MM:SS"
  - 단위: "시간"

**Row 2 (페이스, 속도)**
- **페이스 (분/km)**
  - 형식: "MM:SS"
  - 단위: "페이스 (분/km)"

- **속도 (km/h)**
  - 형식: "X.X"
  - 단위: "속도 (km/h)"

**Row 3 (고저차)**
- **고저차 (m)**
  - 형식: "+XXX"
  - 단위: "고저차 (m)"
  - 중앙 정렬

**Map Area (지도 영역)**
- 타입: `CustomMapView`
- 스타일: `flex: 1` (통계와 컨트롤 사이의 공간)
- 기능:
  - 현재 위치 표시
  - 러닝 경로 표시 (실시간 업데이트)

**Control Container (컨트롤 컨테이너)**
- 타입: `View`
- 위치: 화면 하단 고정
- 스타일:
  - flexDirection: `row`
  - 패딩: `theme.spacing.md`
  - 배경색: `theme.colors.surface`
  - gap: `theme.spacing.sm`

#### 버튼 명세

**"일시정지/재개" 버튼**
- 타입: `Button`
- variant: `outline`
- 스타일: `flex: 1`
- 배경색: 흰색 + 회색 테두리
- 동적 텍스트:
  - `isPaused ? '재개' : '일시정지'`
- 기능:
  - 일시정지 상태: 러닝 재개 (`resumeRunning()`)
  - 실행 중: 러닝 일시정지 (`pauseRunning()`)
- 핸들러: `handlePause()`

**"종료" 버튼**
- 타입: `Button`
- variant: `primary` (주요 버튼, 주황색)
- 스타일: `flex: 1`
- 기능: 러닝 종료 및 결과 화면으로 이동
- 핸들러: `handleFinish()` → `finishRunning()`

---

### 화면 간 네비게이션 흐름

```
MapScreen
  ├─ "코스 생성" 버튼 → CourseGenerationScreen
  └─ "내 코스" 버튼 → CourseListScreen

CourseGenerationScreen
  ├─ "이 코스 사용" 버튼 → MapScreen (생성된 코스 표시)
  └─ "다시 생성" 버튼 → 동일 화면 (코스 재생성)

CourseListScreen
  └─ 코스 카드 클릭 → 코스 상세 화면 (TODO)

RunningScreen
  └─ "종료" 버튼 → 러닝 결과 화면 (TODO)
```

---

### 공통 컴포넌트

#### CustomMapView
- **위치**: 모든 화면에서 사용
- **기능**:
  - 지도 표시
  - 현재 위치 마커
  - 코스 폴리라인 표시
  - 현재 위치 버튼 (선택적)

#### Button
- **variant**: `primary` (주요), `outline` (보조)
- **size**: `small`, `default`
- **fullWidth**: 전체 너비 사용 여부

#### Input
- **label**: 라벨 텍스트
- **placeholder**: 플레이스홀더 텍스트
- **keyboardType**: 키보드 타입
- **error**: 에러 메시지

#### Card
- **elevated**: 그림자 효과
- **onPress**: 클릭 핸들러

#### Loading
- **message**: 로딩 메시지

---

### 스타일 가이드

#### 색상
- **Primary**: 주황색 (`#FF6B35` 또는 RGB: 1, 0.42, 0.21)
- **Background**: 배경색 (`theme.colors.background`)
- **Surface**: 표면 색상 (`theme.colors.surface`, 연한 회색 #fafafa)
- **Text**: 텍스트 색상 (`theme.colors.text`)
- **Text Secondary**: 보조 텍스트 색상 (`theme.colors.textSecondary`)

#### 간격 (Spacing)
- **xs**: 매우 작은 간격
- **sm**: 작은 간격
- **md**: 중간 간격 (16px)
- **lg**: 큰 간격

#### 타이포그래피
- **h1, h2, h3**: 제목 스타일 (h3: 20px, Semi Bold)
- **body**: 본문 스타일 (16px, Regular)
- **caption**: 캡션 스타일 (12px, Regular)
- **button**: 버튼 텍스트 (16px, Semi Bold)
- **statMedium**: 통계 숫자 스타일

#### 버튼 텍스트 중앙 정렬 계산식
- 버튼 너비: 343px
- 버튼 시작 x: 16px
- 버튼 중앙 x: 187.5px
- 텍스트 x = 187.5 - (텍스트 너비 / 2)

#### 버튼 수직 간격
- 버튼 높이: 48px
- 버튼 간 gap: 16px
- 두 번째 버튼 y = 첫 번째 버튼 y + 64

---

### 참고사항

1. **반응형 디자인**: 모든 화면은 375x812 (iPhone 기준) 크기로 설계됨
2. **상태 관리**: Zustand를 사용하여 전역 상태 관리
3. **네비게이션**: React Navigation을 사용하여 화면 전환
4. **테마**: 라이트/다크 모드 지원 (현재는 라이트 모드만 구현)
5. **로딩 상태**: 비동기 작업 시 Loading 컴포넌트 표시
6. **에러 처리**: 에러 발생 시 Alert 또는 에러 메시지 표시
7. **Figma 디자인**: 모든 화면은 Figma에서 디자인 완료 (채널: ra1r3dhi)
8. **최종 확정**: 1~3번째 화면 (MapScreen, CourseGenerationScreen, CourseListScreen)은 최종 확정되어 더 이상 수정하지 않음

