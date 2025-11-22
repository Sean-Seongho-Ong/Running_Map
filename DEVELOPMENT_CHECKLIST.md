# 개발 체크리스트

Running Map App 개발 진행 상황을 관리하는 체크리스트입니다.

## 📊 현재 상태 요약 (2025-11-22)

### 백엔드 완료 현황
- ✅ **도메인 계층**: 완료 (값 객체, 엔티티, 서비스 인터페이스)
- ✅ **Application 계층**: 완료 (DTO, Use Cases, 테스트 46개 통과)
- ✅ **Infrastructure 계층**: 완료 (DB, Redis, OSRM, 테스트 32개 통과)
- ✅ **Interface 계층**: 완료 (API 엔드포인트, 에러 핸들링, 테스트 11개 통과)
- **총 테스트**: 96개 통과 (Infrastructure 32 + Application 46 + Interface 11 + 통합 7)
- ✅ **백엔드 서버**: 실행 중 (`http://localhost:8000`)
- ✅ **샘플 데이터**: 9개 코스 삽입 완료

### 프론트엔드 완료 현황
- ✅ **API 통합**: 완료 (Axios 클라이언트, Repository 패턴, Zustand 연동)
  - ✅ CourseRepository 구현 완료
  - ✅ RunningRepository 구현 완료 (백엔드 응답 형식에 맞게 수정 완료)
  - ✅ API 타입 정의 완료 (백엔드 DTO와 일치)
- ✅ **UI Integration**: 부분 완료
  - ✅ CourseGenerationScreen 연동 (API 호출, 로딩, 에러 처리, 상세 정보 표시)
  - ✅ MapScreen 연동 (생성된 코스 표시, 네비게이션, 지도 제어)
  - ✅ 코스 재생성 기능
  - ✅ UX 개선 (네비게이션 흐름 수정)
  - 🚧 RunningScreen 연동 (기본 구조만, GPS 추적 미구현)
- ✅ **기본 구조**: 완료 (Theme, 컴포넌트, 네비게이션, 화면 레이아웃)
- ✅ **TypeScript 오류**: 수정 완료 (CourseDetailInfo, MapView, Card, Theme)
- ✅ **Android 빌드**: 성공 (compileSdkVersion 34로 업데이트)
- ✅ **Figma 화면 구성**: 완료 (4개 주요 화면 레이아웃 디자인 완료)
  - ✅ MapScreen (지도 메인 화면)
  - ✅ CourseGenerationScreen (코스 생성 화면)
  - ✅ CourseListScreen (코스 목록 화면)
  - ✅ RunningScreen (러닝 추적 화면)
- ✅ **Figma 디자인 코드 적용**: 완료 (모든 화면의 레이아웃, 색상, 크기를 코드에 반영)
  - ✅ Theme 색상 추가 (surfaceLight, mapBackground, borderGray)
  - ✅ Button 컴포넌트 스타일 수정 (outline variant, 버튼 높이)
  - ✅ Card 컴포넌트 스타일 수정 (모서리 8px, 테두리)
  - ✅ 모든 화면 스타일 Figma 디자인에 맞게 조정
- ⚠️ **앱 로드**: Metro Bundler 연결 문제로 인해 앱이 JavaScript 번들을 로드하지 못함

### 최근 완료 작업 (2025-11-22)
- ✅ **Figma 디자인 코드 적용 완료**: 4개 주요 화면의 레이아웃, 색상, 크기를 코드에 반영
  - MapScreen: Map Area 여백, Button Container 스타일, 버튼 크기 조정
  - CourseGenerationScreen: Input Container 배경색, Preset 버튼 크기 조정
  - CourseListScreen: Search Container 높이, 카드 크기 조정
  - RunningScreen: Stats Container, Control Container 패딩 확인
  - Button 컴포넌트: outline variant 스타일, 버튼 높이 조정 (small 40px, medium 48px)
  - Card 컴포넌트: 모서리 8px, 테두리 스타일 추가
  - Theme 색상: surfaceLight (#fafafa), mapBackground (#d9d9d9), borderGray (#e0e0e0) 추가
- ✅ **Figma 화면 구성 완료**: 4개 주요 화면 레이아웃 디자인 완료
  - MapScreen, CourseGenerationScreen, CourseListScreen, RunningScreen
- ✅ **프론트엔드 API 코드 검토 및 수정 완료**
  - RunningRepository 응답 처리 수정 (백엔드 응답 형식에 맞게)
  - API 타입 정의 추가 (RunningSessionStartResponse 등)
  - Location Update 요청 형식 수정 (timestamp 필드 추가)
  - Finish Running 요청 형식 수정 (route 필드 제거)

### 남은 주요 작업

#### 우선순위 1: 프론트엔드 앱 로드 문제 해결 (즉시 필요)
1. **Metro Bundler 연결 문제 해결**
   - **결정**: Android Studio + Expo Dev Client 유지 (네이티브 모듈 필수)
   - **해결 방법**:
     - 캐시 클리어: `expo start -c --dev-client`
     - 네트워크 설정 확인: 방화벽 포트 8081 허용
     - 포트 포워딩: `adb reverse tcp:8081 tcp:8081`
     - WebSocket 연결 테스트
   - **목표**: 앱이 정상적으로 JavaScript 번들을 로드하고 실행됨

#### 우선순위 2: 앱 기능 테스트 (앱 로드 후)
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

#### 우선순위 3: 러닝 추적 기능 구현
4. **GPS 위치 추적 구현** (프론트엔드)
   - 위치 권한 요청
   - GPS 위치 추적 시작/중지
   - 주기적 위치 업데이트 (예: 5초마다)
   - 위치 정확도 필터링
5. **실시간 통계 계산** (프론트엔드)
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

#### 우선순위 4: 코스 관리 기능 완성
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

#### 우선순위 5: 코스 생성 알고리즘 구현 (백엔드)
10. **DistanceConstrainedLoopGenerator 구현**
    - Step 기반 원둘레 분할
    - 양방향 Adaptive Step 피드백
    - S-P 기반 Fallback
    - 도로 스냅핑 로직
    - 루프 폐쇄 검증
    - 자가 교차 검증
    - 알고리즘 단위 테스트 작성

---

## 📋 백엔드 개발

### 개발 환경 설정
- [x] Conda 환경 생성 (running_map)
- [x] Python 의존성 설치 (requirements.txt)
- [x] 환경 설정 파일 업데이트 (environment.yml)
- [x] 백엔드 프로젝트 구조 생성 (Clean Architecture)
- [x] 기본 설정 파일 생성 (main.py, config.py, alembic.ini)

### 인프라 설정
- [x] Docker Compose 환경 구성 (PostgreSQL, Redis, OSRM)
- [x] 환경 변수 설정 (.env)
- [x] 데이터베이스 마이그레이션 설정 (Alembic)
- [x] 초기 마이그레이션 생성 및 적용 (`9d86b00d0532_initial_migration.py`)
- [x] Redis 연결 테스트
- [ ] OSRM 서버 연결 테스트 (클라이언트 구현 완료)

### 도메인 계층
- [x] `Coordinate` 값 객체 구현
- [x] `Distance` 값 객체 구현
- [x] `Course` 엔티티 구현
- [x] `RunningSession` 엔티티 구현
- [x] `Route` 엔티티 구현
- [x] 도메인 서비스 인터페이스 정의 (LoopGenerator, RouteCalculator, DistanceCalculator)
- [x] 리포지토리 인터페이스 정의 (CourseRepository, RunningSessionRepository)

### 코스 생성 알고리즘
- [ ] Step 기반 원둘레 분할 구현
- [ ] 양방향 Adaptive Step 피드백 구현
- [ ] S-P 기반 Fallback 구현
- [ ] 도로 스냅핑 로직 구현
- [ ] 루프 폐쇄 검증 구현
- [ ] 자가 교차 검증 구현
- [ ] 알고리즘 단위 테스트 작성

### 인프라 계층
- [x] PostgreSQL + PostGIS 연결 설정
- [x] SQLAlchemy 모델 정의 (CourseModel, RunningSessionModel)
- [x] 리포지토리 구현 (Course, RunningSession)
  - [x] CRUD 메서드 구현
  - [x] 에러 처리 강화 (트랜잭션 롤백, 커스텀 예외)
  - [x] 쿼리 최적화 (인덱스 활용, 필드 선택, N+1 방지)
- [x] OSRM 클라이언트 구현
  - [x] 경로 계산 및 거리 계산
  - [x] 재시도 로직 (exponential backoff)
  - [x] Rate limiting 처리
  - [x] 타임아웃 처리
- [x] Redis 캐시 래퍼 구현
  - [x] 기본 캐시 메서드 (get, set, delete, exists)
  - [x] 코스 생성 결과 캐싱 (TTL: 24시간)
  - [x] 라우팅 결과 캐싱 (TTL: 7일)
- [x] 공간 인덱스 설정 (GIST)
  - [x] courses.polyline GIST 인덱스
  - [x] running_sessions.route_polyline GIST 인덱스

### Application 계층
- [x] DTO 정의
  - [x] Course DTO (CourseGenerationRequest, CourseGenerationResponse, CourseSaveRequest 등)
  - [x] Running DTO (RunningSessionStartRequest, RunningSessionStartResponse 등)
- [x] 코스 관련 Use Cases
  - [x] 코스 생성 Use Case (캐시 확인, LoopGenerator 호출, 결과 캐싱)
  - [x] 코스 저장 Use Case
  - [x] 코스 목록 조회 Use Case
  - [x] 코스 상세 조회 Use Case
  - [x] 코스 삭제 Use Case
- [x] 러닝 관련 Use Cases
  - [x] 러닝 시작 Use Case
  - [x] 러닝 업데이트 Use Case
  - [x] 위치 업데이트 Use Case
  - [x] 러닝 종료 Use Case
- [x] Application 계층 테스트
  - [x] DTO 단위 테스트 (25개 통과)
  - [x] Use Cases 단위 테스트 (21개 통과)

### API 계층 (Interface)
- [x] FastAPI 앱 초기화 (main.py)
- [x] CORS 설정
- [x] API 라우터 구조 생성 (interface/api/ 폴더)
- [x] 코스 생성 API (`POST /api/v1/courses/generate`)
- [x] 코스 저장 API (`POST /api/v1/courses`)
- [x] 코스 목록 API (`GET /api/v1/courses`)
- [x] 코스 상세 API (`GET /api/v1/courses/{id}`)
- [x] 코스 삭제 API (`DELETE /api/v1/courses/{id}`)
- [x] 러닝 시작 API (`POST /api/v1/running/start`)
- [x] 러닝 업데이트 API (`PUT /api/v1/running/{session_id}`)
- [x] 위치 업데이트 API (`POST /api/v1/running/{session_id}/location`)
- [x] 러닝 종료 API (`POST /api/v1/running/{session_id}/finish`)
- [x] API 스키마 정의 (Pydantic) - DTO 재사용
- [x] 에러 핸들링 구현
- [x] 의존성 주입 설정 (Use Cases, Repositories)
- [x] API 문서화 (Swagger/ReDoc) - OpenAPI 명세서 작성 완료 (`plan/api-specification.yaml`)

### 테스트
- [x] 도메인 로직 단위 테스트
- [ ] 코스 생성 알고리즘 테스트
- [x] 리포지토리 테스트 (11개 테스트 통과)
- [x] 인프라 계층 테스트 (32개 테스트 통과)
  - [x] Redis 캐시 테스트 (14개)
  - [x] OSRM 클라이언트 테스트 (7개)
  - [x] 리포지토리 테스트 (11개)
- [x] Application 계층 테스트 (46개 테스트 통과)
  - [x] DTO 테스트 (25개)
  - [x] Use Cases 테스트 (21개)
- [x] 통합 테스트
  - [x] Redis 통합 테스트 (6개 테스트 통과)
  - [x] 데이터베이스 연결 테스트 (기본 연결 확인 성공)
  - [x] PostGIS WKB 변환 로직 구현 (shapely 사용)
  - [ ] 데이터베이스 CRUD 통합 테스트 (Windows 환경 제약으로 일부 실패, Linux 환경에서 정상 동작 예상)
- [x] API 엔드포인트 테스트 (11개 테스트 통과)
  - [x] Course API 테스트 (7개 통과)
  - [x] Running API 테스트 (4개 통과)
- [ ] 성능 테스트 (부하 테스트)

### 디버깅 및 이슈 해결

#### Windows 환경 이슈
- [ ] 데이터베이스 CRUD 통합 테스트 디버깅
  - **문제**: Windows 환경에서 asyncpg와 ProactorEventLoop 호환성 문제로 일부 통합 테스트 실패
  - **증상**: `InterfaceError: cannot perform operation: another operation is in progress`
  - **영향**: 데이터베이스 CRUD 통합 테스트 (CourseRepository, RunningSessionRepository)
  - **예상 원인**: Windows의 ProactorEventLoop와 asyncpg의 비동기 처리 충돌
  - **해결 방안**:
    - [ ] Linux 환경에서 테스트 실행하여 정상 동작 확인
    - [ ] pytest-asyncio 설정 조정 (이벤트 루프 정책 변경)
    - [ ] 각 테스트마다 독립적인 세션 생성 보장
    - [ ] Windows 환경에서도 동작하도록 세션 관리 로직 개선
  - **참고**: 단위 테스트는 모두 통과했으며, 핵심 로직은 검증 완료

#### 프론트엔드 앱 로드 문제 (2025-11-22)
- [ ] Metro Bundler 연결 문제 해결
  - **문제**: Android Studio에서 빌드는 성공했지만 앱이 JavaScript 번들을 로드하지 못함
  - **증상**: 
    - 앱이 Expo Dev Client 화면에서 멈춤
    - Metro Bundler는 정상 실행 중이지만 번들 요청이 없음
    - WebSocket 연결 오류 발생 (`Connection reset`)
  - **시도한 해결 방법**:
    - [x] TypeScript 오류 수정 완료 (CourseDetailInfo, MapView, Card, Theme)
    - [x] Android SDK 버전 업데이트 (compileSdkVersion 34)
    - [x] Metro config.js 파일 생성
    - [x] package.json 스크립트 수정 (Expo Go 방식으로 변경 시도)
  - **발견된 제약사항**:
    - `react-native-maps`: Expo Go에서 지원하지 않음
    - `@react-native-community/geolocation`: Expo Go에서 지원하지 않음
  - **해결 방안**:
    - [ ] Expo Dev Client 방식 유지 (권장)
      - [ ] Metro Bundler 연결 문제 디버깅
      - [ ] WebSocket 연결 문제 해결
      - [ ] 앱이 정상적으로 번들을 로드하도록 수정
    - [ ] 또는 Expo Go 호환 모듈로 교체
      - [ ] `react-native-maps` → `expo-location` + Expo Maps API
      - [ ] `@react-native-community/geolocation` → `expo-location`
  - **다음 단계**:
    1. Metro Bundler를 Expo CLI로 재시작 (`expo start -c --dev-client`)
    2. Expo Dev Client에서 서버 연결 확인
    3. WebSocket 연결 문제 해결
    4. 앱이 정상적으로 로드되는지 확인
  - **권장 사항**: Android Studio + Expo Dev Client 유지
    - 네이티브 모듈 필수 (`react-native-maps`, `@react-native-community/geolocation`)
    - 빌드는 이미 성공했으므로 연결 문제만 해결하면 됨
    - Expo Go로 전환 시 대규모 코드 수정 필요 (비권장)
  - **참고**: 
    - Android Studio 빌드는 성공했으며, 네이티브 코드는 정상 작동
    - 문제는 JavaScript 번들 로딩 단계에서 발생
    - Expo Go 방식으로 전환 시도했지만 네이티브 모듈 호환성 문제로 중단
    - Expo Dev Client 방식 유지 필요

### 최적화
- [x] 코스 생성 결과 캐싱 (Redis) - TTL: 24시간
- [x] 라우팅 결과 캐싱 (Redis) - TTL: 7일
- [x] 데이터베이스 쿼리 최적화
  - [x] 인덱스 활용 (user_id, is_public, created_at)
  - [x] 필요한 필드만 선택 (`select_fields` 파라미터)
  - [x] N+1 문제 방지 (`load_relationships` 파라미터 준비)
- [x] 공간 인덱스 최적화 (GIST 인덱스 생성 완료)
- [x] 비동기 처리 최적화 (모든 I/O 작업 비동기 처리)

---

## 📱 프론트엔드 개발 (React Native)

### 개발 환경 설정
- [x] Node.js 의존성 설치 (npm install)
- [x] Bun 설치 (패키지 매니저)

### 프로젝트 설정
- [x] Expo Bare Workflow 프로젝트 초기화
- [x] iOS/Android 네이티브 설정
- [x] TypeScript 설정
- [x] ESLint/Prettier 설정
- [x] 환경 변수 설정
- [x] Android 빌드 설정 (compileSdkVersion 34)
- [x] Metro config.js 설정
- [x] TypeScript 오류 수정

### 디자인 시스템
- [x] Theme 시스템 구현 (colors, typography, spacing)
- [x] 공통 컴포넌트 구현 (Button, Input, Card, Loading)
- [ ] 아이콘 라이브러리 통합
- [ ] 다크 모드 지원

### 지도 기능
- [x] MapView 컴포넌트 구현
- [x] CoursePolyline 컴포넌트 구현
- [x] LocationMarker 컴포넌트 구현
- [ ] OSM 타일 서버 연동 (TileServer GL)
- [ ] 지도 줌/팬 제어
- [ ] 지도 중심점 설정
- [ ] 지도 스타일 커스터마이징
- [ ] 오프라인 지도 캐싱 (선택사항)

### 코스 생성 기능
- [x] 거리 입력 UI
- [x] 코스 생성 파라미터 입력 UI (기본 거리만 구현)
- [x] 백엔드 API 연동
- [x] 코스 생성 로딩 상태 표시
- [x] 생성된 코스 지도 표시
- [x] 코스 상세 정보 표시 (CourseDetailInfo 컴포넌트)
- [x] 코스 재생성 기능
- [x] 코스 생성 실패 처리
- [x] UX 개선 (네비게이션 흐름 수정)

### 코스 관리 기능
- [ ] 코스 목록 화면
- [ ] 코스 검색 기능
- [ ] 코스 저장 기능
- [ ] 코스 로드 기능
- [ ] 코스 삭제 기능
- [ ] 코스 공유 기능 (향후)
- [ ] AsyncStorage 연동

### 러닝 추적 기능
- [ ] 위치 권한 요청
- [ ] GPS 위치 추적 구현
- [ ] 러닝 세션 시작/종료
- [ ] 실시간 통계 계산 (거리, 시간, 페이스, 속도)
- [ ] 고저차 계산 (가속도계/기압계 활용)
- [ ] 러닝 경로 기록
- [ ] 러닝 데이터 표시 UI
- [ ] 백엔드 동기화

### 상태 관리
- [x] Zustand 스토어 구조 생성
- [x] courseStore 구현
- [x] runningStore 구현
- [x] locationStore 구현
- [x] API 통합 상태 관리
- [ ] 오프라인 상태 관리

### 네비게이션
- [x] React Navigation 설정
- [x] Bottom Tab Navigator 구현
- [x] Stack Navigator 구현
- [x] 화면 기본 레이아웃 구현
- [ ] 화면 간 데이터 전달
- [ ] 딥링크 설정 (선택사항)

### 화면 구현
- [x] MapScreen 기본 레이아웃
- [x] CourseGenerationScreen 기본 레이아웃
- [x] RunningScreen 기본 레이아웃
- [x] CourseListScreen 기본 레이아웃
- [x] MapScreen 기능 완성 (코스 표시, 네비게이션, 지도 제어)
- [x] CourseGenerationScreen 기능 완성 (API 연동, 로딩, 에러 처리, 상세 정보 표시, 재생성)
- [x] **Figma 화면 구성 디자인 완료** (채널: ra1r3dhi)
  - 4개 주요 화면 레이아웃 디자인 완료
  - 화면 구조 및 컴포넌트 배치 검토 가능
- [x] **Figma 디자인 코드 적용 완료**
  - 모든 화면의 레이아웃, 색상, 크기를 Figma 디자인에 맞게 코드에 반영
  - Theme 색상 추가 및 컴포넌트 스타일 수정 완료
- [ ] RunningScreen 기능 완성 (GPS 추적 미구현)
- [ ] CourseListScreen 기능 완성 (API 연동 필요)
- [ ] 프로필 화면 (향후)
- ⚠️ **앱 로드 문제**: Android Studio 빌드는 성공했지만 앱이 JavaScript 번들을 로드하지 못함

### 성능 최적화
- [ ] React.memo 적용
- [ ] useMemo/useCallback 최적화
- [ ] 지도 렌더링 최적화
- [ ] 이미지 최적화
- [ ] 번들 크기 최적화

### 테스트
- [ ] 컴포넌트 단위 테스트
- [ ] 훅 테스트
- [ ] 통합 테스트
- [ ] E2E 테스트 (선택사항)

---

## 🎨 Figma 디자인

### 사용자 플로우
- [x] 코스 생성 플로우 다이어그램
- [x] 러닝 추적 플로우 다이어그램

### 와이어프레임
- [x] MapScreen 와이어프레임
- [x] CourseGenerationScreen 와이어프레임
- [x] RunningScreen 와이어프레임
- [x] CourseListScreen 와이어프레임

### 디자인 시스템
- [x] 색상 팔레트 정의
- [x] 타이포그래피 정의
- [x] 간격 시스템 정의
- [x] 버튼 스타일 정의
- [x] 입력 필드 스타일 정의

### 하이파이 프로토타입
- [x] MapScreen 하이파이
- [x] CourseGenerationScreen 하이파이
- [x] RunningScreen 하이파이
- [x] CourseListScreen 하이파이
- [ ] 기본 인터랙션 연결

### Figma MCP 연동
- [x] Figma MCP 서버 연결 설정
- [x] 채널 연결 테스트 (채널: ra1r3dhi)
- [x] 기본 기능 테스트 (요소 생성, 수정, 읽기)
- [x] 4개 주요 화면 레이아웃 디자인 완료
  - [x] MapScreen (지도 메인 화면)
  - [x] CourseGenerationScreen (코스 생성 화면)
  - [x] CourseListScreen (코스 목록 화면)
  - [x] RunningScreen (러닝 추적 화면)

---

## 🔗 통합 및 연동

### API 통합
- [x] 백엔드 API 클라이언트 구현
  - [x] Axios 설치 및 설정
  - [x] API Client 구현 (인터셉터, 에러 핸들링, 로깅)
  - [x] API 엔드포인트 상수 정의
  - [x] TypeScript 타입 정의 (백엔드 DTO와 일치)
- [x] CourseRepository 구현 (generateCourse, saveCourse, listCourses, getCourse)
- [x] RunningRepository 구현 (startRunning, updateLocation, finishRunning)
  - [x] 백엔드 응답 형식에 맞게 수정 완료 (ApiResponse 래퍼 제거, 필드명 매핑)
- [x] Zustand 스토어와 Repository 연동
  - [x] courseStore.ts 업데이트
  - [x] runningStore.ts 업데이트
- [ ] 인증 처리 (향후)
- [x] 에러 핸들링
- [x] 로깅 규칙 준수 (Logger 유틸리티 사용)
- [ ] 재시도 로직
- [ ] 타임아웃 처리

### UI Integration
- [x] CourseGenerationScreen 연동
  - [x] API 호출 연동
  - [x] 로딩 상태 표시
  - [x] 에러 처리 및 알림
  - [x] 성공 시 MapScreen으로 네비게이션
- [x] MapScreen 연동
  - [x] 생성된 코스 지도 표시
  - [x] 네비게이션 연결
- [ ] RunningScreen 연동
  - [ ] GPS 위치 추적 시작
  - [ ] 주기적 위치 업데이트
  - [ ] 러닝 세션 시작/종료

### 데이터 동기화
- [ ] 코스 데이터 동기화
- [ ] 러닝 세션 데이터 동기화
- [ ] 오프라인 모드 지원 (선택사항)

### 테스트
- [ ] 백엔드-프론트엔드 통합 테스트
- [ ] API 통합 테스트
- [ ] 데이터 흐름 검증

---

## 🚀 배포

### 백엔드 배포
- [ ] 프로덕션 환경 설정
- [ ] 데이터베이스 마이그레이션
- [ ] 환경 변수 설정
- [ ] Docker 이미지 빌드
- [ ] 서버 배포
- [ ] HTTPS 설정
- [ ] 도메인 연결
- [ ] 모니터링 설정

### 프론트엔드 배포
- [ ] Android 빌드 설정
- [ ] iOS 빌드 설정
- [ ] 앱 서명 설정
- [ ] Google Play 스토어 등록 (향후)
- [ ] Apple App Store 등록 (향후)

### 인프라
- [ ] OSRM 서버 배포
- [ ] TileServer GL 배포
- [ ] Redis 클러스터 설정
- [ ] 로드 밸런서 설정
- [ ] CDN 설정 (선택사항)

---

## 📝 문서화

- [x] 프로젝트 README
- [x] 백엔드 README
- [x] 프론트엔드 README
- [x] API 명세서 작성 (OpenAPI 3.0 - `plan/api-specification.yaml`)
- [x] README 파일 일관성 검증 및 업데이트
- [x] 설계 문서 업데이트 (SDS_Running_App.md, Frontend_Architecture_Design.md)
- [ ] API 문서 (Swagger/ReDoc) - 서버 실행 시 자동 생성 (명세서 기반)
- [ ] 개발 가이드
- [ ] 배포 가이드
- [ ] 사용자 가이드 (향후)

---

## 진행 상황

- **완료**: ✅
- **진행 중**: 🚧
- **미시작**: ⬜

### 현재 상태
- ✅ 프로젝트 구조 설계 완료
- ✅ 백엔드 프로젝트 구조 생성 (Clean Architecture)
- ✅ 백엔드 도메인 계층 구현 완료
  - 값 객체: Coordinate, Distance
  - 엔티티: Course, RunningSession, Route
  - 도메인 서비스 인터페이스: LoopGenerator, RouteCalculator, DistanceCalculator
  - 리포지토리 인터페이스: CourseRepository, RunningSessionRepository
- ✅ API 명세서 작성 완료 (OpenAPI 3.0)
- ✅ FastAPI 기본 설정 완료 (main.py, config.py, CORS)
- ✅ Alembic 마이그레이션 기본 설정 완료
- ✅ Theme 시스템 구현 완료
- ✅ 기본 컴포넌트 구현 완료
- ✅ 상태 관리 구조 완료
- ✅ 네비게이션 구조 완료
- ✅ 화면 기본 레이아웃 완료
- ✅ 백엔드 개발 환경 설정 완료 (Conda 환경, 의존성 설치)
- ✅ 프론트엔드 개발 환경 설정 완료 (의존성 설치, Bun 설치)
- ✅ Figma MCP 연동 완료
- ✅ 문서화 완료 (README 파일들, 설계 문서 업데이트)
- ✅ API 엔드포인트 구현 완료 (Interface 계층 테스트 11개 통과)
- ✅ 프론트엔드 API 통합 완료
  - API 클라이언트 구현 (Axios, 로깅 규칙 준수)
  - Repository 패턴 구현 (Course, Running)
  - Zustand 스토어 연동
  - 백엔드 응답 형식에 맞게 수정 완료 (RunningRepository)
- ✅ UI 화면 연동 부분 완료
  - CourseGenerationScreen 연동 완료 (API 호출, 로딩, 에러 처리, 상세 정보 표시, 재생성)
  - MapScreen 연동 완료 (코스 표시, 네비게이션, 지도 제어)
  - UX 개선 완료 (네비게이션 흐름 수정)
- ✅ TypeScript 오류 수정 완료
- ✅ Android 빌드 성공 (compileSdkVersion 34)
- ✅ Figma 화면 구성 디자인 완료 (4개 주요 화면)
  - MapScreen, CourseGenerationScreen, CourseListScreen, RunningScreen
- ⚠️ 프론트엔드 앱 로드 문제 (Metro Bundler 연결)
- 🚧 코스 생성 알고리즘 구현 필요
- 🚧 RunningScreen 완전 연동 필요 (GPS 추적 구현)
- ⬜ 러닝 추적 기능 구현 필요

---

## 참고

- [SRS 문서](plan/SRS_Running_App.md)
- [SDS 문서](plan/SDS_Running_App.md)
- [API 명세서](plan/api-specification.yaml) - OpenAPI 3.0 형식
- [기술 스택 결정](plan/SRS_Technology_Decisions.md)
- [프론트엔드 아키텍처](plan/Frontend_Architecture_Design.md)
- [코스 생성 알고리즘](plan/distance_constrained_loop_v1_0.md)

