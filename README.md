# Running Map App

러닝 코스 자동 생성 및 추적 모바일 애플리케이션

## 프로젝트 개요

이 프로젝트는 사용자가 원하는 거리를 입력하면 자동으로 러닝 코스를 생성하고, 러닝 중 실시간으로 속도, 페이스, 고저차 등의 정보를 제공하는 모바일 애플리케이션입니다.

### 주요 기능

- 📍 **지도 기반 코스 생성**: 사용자 위치 기반으로 거리 제약 루프 생성
- 🏃 **러닝 추적**: 실시간 속도, 페이스, 고저차 측정
- 💾 **코스 저장 및 관리**: 생성된 코스 저장, 로드, 공유
- 🗺️ **OpenStreetMap 기반**: OSM 데이터를 활용한 자체 지도 서비스

### 기술 스택

**모바일 앱:**
- React Native (TypeScript) + Expo Bare Workflow
- react-native-maps (OSM 타일)
- Zustand (상태 관리)
- React Navigation

**백엔드:**
- Python 3.11+ + FastAPI
- PostgreSQL + PostGIS
- Redis (캐싱)
- OSRM (라우팅)

**인프라:**
- Docker Compose (로컬 개발)
- TileServer GL (지도 타일)

## 프로젝트 구조

```
Running_map/
├── plan/                          # 설계 문서
│   ├── SRS_Running_App.md        # 소프트웨어 요구사항 명세
│   ├── SDS_Running_App.md        # 시스템 설계 명세
│   ├── SRS_Technology_Decisions.md
│   ├── UI_UX_Design_Plan.md
│   ├── Frontend_Architecture_Design.md
│   ├── Figma_Design_Guide.md
│   ├── OSM_ReactNative_Options.md
│   ├── distance_constrained_loop_v1_0.md  # 코스 생성 알고리즘
│   └── api-specification.yaml     # OpenAPI 3.0 API 명세서
│
├── backend/                        # 백엔드 (Python + FastAPI)
│   ├── domain/                     # 도메인 계층 (구현 완료)
│   │   ├── entities/               # 엔티티: Course, RunningSession, Route
│   │   ├── value_objects/          # 값 객체: Coordinate, Distance
│   │   ├── services/               # 도메인 서비스 인터페이스
│   │   └── repositories/           # 리포지토리 인터페이스
│   ├── application/                # 유즈케이스 (향후 구현)
│   ├── infrastructure/            # 인프라스트럭처 (구현 완료)
│   │   ├── database/               # 데이터베이스 (SQLAlchemy + PostGIS)
│   │   ├── external/               # 외부 API (OSRM 클라이언트)
│   │   ├── cache/                  # 캐시 (Redis)
│   │   └── exceptions.py          # 커스텀 예외
│   ├── interface/                 # API 인터페이스 (향후 구현)
│   ├── alembic/                   # 데이터베이스 마이그레이션
│   ├── main.py                    # FastAPI 앱 진입점
│   ├── config.py                  # 환경 변수 설정
│   ├── requirements.txt
│   └── README.md
│
├── mobile/                         # 모바일 앱 (React Native)
│   ├── src/
│   │   ├── domain/                 # 도메인 계층 (엔티티, 값 객체)
│   │   ├── interface/              # UI 계층 (컴포넌트, 화면, 네비게이션, 스토어)
│   │   └── theme/                  # 디자인 시스템
│   ├── cursor-talk-to-figma-mcp/   # Figma MCP 통합 도구
│   ├── App.tsx                     # 앱 진입점
│   ├── package.json
│   └── README.md
│
├── docker-compose.yml             # Docker Compose 설정
├── .env.example                   # 환경 변수 예시
└── DEVELOPMENT_CHECKLIST.md       # 개발 체크리스트
```

## 빠른 시작

### 사전 요구사항

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

### 1. 저장소 클론

```bash
git clone https://github.com/Sean-Seongho-Ong/Running_Map.git
cd Running_Map
```

### 2. 환경 변수 설정

```bash
# 백엔드 환경 변수 설정
cd backend
# .env 파일을 생성하고 필요한 설정을 변경하세요
# 주요 설정: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, REDIS_HOST, REDIS_PORT

# 모바일 앱 환경 변수 (선택사항)
cd ../mobile
# src/infrastructure/config/api.ts에서 API_BASE_URL 설정
```

### 3. 인프라 서비스 시작 (Docker Compose)

```bash
# PostgreSQL, Redis, OSRM 시작
docker-compose up -d postgres redis osrm

# TileServer GL (선택사항)
docker-compose --profile tileserver up -d tileserver
```

### 4. 백엔드 설정

```bash
cd backend

# 방법 1: Conda 사용 (권장)
conda env create -f environment.yml
conda activate running_map

# 방법 2: Python venv 사용
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 환경 변수 설정 (.env 파일 생성)
# .env.example을 참고하여 .env 파일을 생성하세요

# Docker Compose 서비스 시작 (PostgreSQL, Redis)
cd ..
docker-compose up -d postgres redis
cd backend

# 데이터베이스 마이그레이션 (모델 정의 후)
# alembic revision --autogenerate -m "Initial migration"
# alembic upgrade head

# 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**참고**: 현재는 도메인 계층만 구현되어 있어 데이터베이스 모델이 아직 정의되지 않았습니다.

### 5. 모바일 앱 설정

```bash
cd mobile

# 의존성 설치
npm install

# iOS 의존성 설치 (macOS만)
cd ios && pod install && cd ..

# 개발 서버 시작
npm start

# 또는 직접 실행
# Android
npm run android

# iOS
npm run ios
```

## 개발 가이드

### 설계 문서

모든 설계 문서는 `plan/` 폴더에 있습니다:

- **SRS_Running_App.md**: 소프트웨어 요구사항 명세
- **SDS_Running_App.md**: 시스템 설계 명세
- **api-specification.yaml**: OpenAPI 3.0 API 명세서 (완전한 API 스펙)
- **SRS_Technology_Decisions.md**: 기술 스택 결정 사항
- **UI_UX_Design_Plan.md**: UI/UX 설계 계획
- **Frontend_Architecture_Design.md**: 프론트엔드 아키텍처
- **Figma_Design_Guide.md**: Figma 디자인 가이드
- **distance_constrained_loop_v1_0.md**: 코스 생성 알고리즘

### 코딩 규칙

프로젝트 코딩 규칙은 `.cursor/rules/architecture.mdc`에 정의되어 있습니다.

주요 원칙:
- SOLID 원칙 준수
- Clean Architecture 기반 구조
- 하드코딩 방지
- Git 기반 버전 관리

### 개발 체크리스트

`DEVELOPMENT_CHECKLIST.md`를 참고하여 개발 진행 상황을 관리하세요.

## 주요 기능 상세

### 코스 생성 알고리즘

Distance-Constrained Loop Generation Algorithm v1.0을 사용합니다:
- Step 기반 원둘레 분할
- 양방향 Adaptive Step 피드백
- S-P 기반 Fallback

자세한 내용은 `plan/distance_constrained_loop_v1_0.md` 참고.

### 지도 및 라우팅

- **지도**: OSM + react-native-maps + TileServer GL
- **라우팅**: OSRM (로컬 서버)

## 환경별 구성

### 개발 환경 (로컬)

```bash
# Docker Compose로 모든 서비스 실행
docker-compose up -d

# 백엔드 서버 (로컬)
cd backend && uvicorn main:app --reload

# 모바일 앱 (Expo Dev Client)
cd mobile && npm start
```

### 프로토타입 환경

- VPS 또는 로컬 서버에서 Docker Compose로 실행
- Nginx 리버스 프록시 설정
- HTTPS (Let's Encrypt)

### 프로덕션 환경

- 클라우드 서비스 (AWS/GCP) 사용 고려
- 관리형 데이터베이스 (RDS, Cloud SQL)
- 관리형 Redis (ElastiCache, Memorystore)

## API 문서

### OpenAPI 명세서

완전한 API 명세서는 `plan/api-specification.yaml`에 정의되어 있습니다.

- **OpenAPI 3.0 형식**: Swagger Editor에서 확인 가능
- **모든 엔드포인트 정의**: 요청/응답 스키마, 에러 응답 포함
- **FastAPI 자동 문서화**: 서버 실행 시 자동 생성

### API 문서 확인

백엔드 서버 실행 후 다음 URL에서 API 문서 확인:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 주요 API 엔드포인트

- **코스 생성**: `POST /api/v1/courses/generate`
- **코스 관리**: `POST /api/v1/courses`, `GET /api/v1/courses`, `GET /api/v1/courses/{id}`, `DELETE /api/v1/courses/{id}`
- **러닝 추적**: `POST /api/v1/running/start`, `PUT /api/v1/running/{session_id}`, `POST /api/v1/running/{session_id}/finish`

자세한 내용은 `plan/api-specification.yaml` 참고.

## 테스트

### 백엔드 테스트

```bash
cd backend

# 전체 테스트
pytest

# 통합 테스트 (실제 데이터베이스/Redis 연결 필요)
pytest -m integration

# 커버리지 포함
pytest --cov=backend --cov-report=html
```

**테스트 결과**:
- Infrastructure 계층: 32개 통과
- Application 계층: 46개 통과 (DTO: 25개, Use Cases: 21개)
- Interface 계층: 11개 통과 (Course API: 7개, Running API: 4개)
- 통합 테스트: 7개 통과 (Redis: 6개, DB 연결: 1개)
- **총 96개 테스트 통과**

**최근 업데이트 (2025-11-22)**:
- ✅ Figma 디자인 코드 적용 완료 (모든 화면의 레이아웃, 색상, 크기 반영)
- ✅ Figma 화면 구성 디자인 완료 (4개 주요 화면)
- ✅ 프론트엔드 API 코드 검토 및 수정 완료 (RunningRepository, 타입 정의)

### 프론트엔드 테스트

```bash
cd mobile
npm test
```

## 배포

배포 관련 정보는 `DEVELOPMENT_CHECKLIST.md`의 배포 섹션을 참고하세요.

## 문제 해결

### 일반적인 문제

1. **Docker 컨테이너가 시작되지 않음**
   - Docker가 실행 중인지 확인
   - 포트 충돌 확인 (`docker-compose.yml`에서 포트 변경)

2. **데이터베이스 연결 실패**
   - `.env` 파일의 DB 설정 확인
   - PostgreSQL 컨테이너 상태 확인: `docker-compose ps`

3. **OSRM 서비스 오류**
   - OSM 데이터 파일이 준비되었는지 확인
   - `osrm-data/` 폴더에 데이터 파일 존재 확인

4. **모바일 앱 빌드 실패**
   - `node_modules` 삭제 후 재설치: `rm -rf node_modules && npm install`
   - iOS: `cd ios && pod install`
   - Expo 캐시 정리: `expo start -c`

## 기여 가이드

1. 기능 브랜치 생성: `git checkout -b feature/your-feature`
2. 변경사항 커밋: `git commit -m "feat: your feature"`
3. 브랜치 푸시: `git push origin feature/your-feature`
4. Pull Request 생성

## 라이선스

[라이선스 정보]

## 현재 개발 상태

### 완료된 작업 ✅

- ✅ 프로젝트 구조 설계 및 생성
- ✅ API 명세서 작성 (OpenAPI 3.0)
- ✅ 백엔드 도메인 계층 구현
  - 값 객체: Coordinate, Distance
  - 엔티티: Course, RunningSession, Route
  - 도메인 서비스 인터페이스
  - 리포지토리 인터페이스
- ✅ 백엔드 인프라 계층 구현
  - SQLAlchemy 모델 정의 (Course, RunningSession)
  - 리포지토리 구현 (CRUD + 에러 처리)
  - OSRM 클라이언트 (재시도 로직, Rate limiting)
  - Redis 캐시 (코스 및 라우팅 결과 캐싱)
  - 데이터베이스 마이그레이션 (Alembic)
  - 쿼리 최적화 (인덱스 활용, 필드 선택, N+1 방지)
  - PostGIS WKB 변환 로직 (shapely 사용)
  - 단위 테스트 (32개 테스트 통과)
  - 통합 테스트 (Redis: 6개 통과, DB 연결: 1개 통과)
- ✅ 백엔드 Application 계층 구현
  - DTO 정의 (Course, Running 관련 모든 DTO)
  - Use Cases 구현 (코스 관련 5개, 러닝 관련 4개)
  - 단위 테스트 (46개 테스트 통과)
- ✅ 백엔드 Interface 계층 구현
  - API 엔드포인트 (Course, Running)
  - Pydantic 스키마 및 에러 핸들링
  - API 테스트 (11개 통과)
- ✅ 프론트엔드 기본 구조 (Theme, 컴포넌트, 네비게이션)
- ✅ 프론트엔드 API 통합
  - Axios 클라이언트 구현 (로깅 규칙 준수)
  - Repository 패턴 (Course, Running)
  - Zustand 스토어 연동
  - 백엔드 응답 형식에 맞게 수정 완료 (RunningRepository)
- ✅ UI Integration 부분 완료
  - CourseGenerationScreen 연동 (API 호출, 로딩, 에러 처리, 상세 정보 표시, 재생성)
  - MapScreen 연동 (생성된 코스 표시, 네비게이션, 지도 제어)
  - UX 개선 (네비게이션 흐름 수정)
- ✅ Figma MCP 연동
- ✅ **Figma 화면 구성 디자인 완료** (채널: ra1r3dhi)
  - MapScreen (지도 메인 화면)
  - CourseGenerationScreen (코스 생성 화면)
  - CourseListScreen (코스 목록 화면)
  - RunningScreen (러닝 추적 화면)
- ✅ **Figma 디자인 코드 적용 완료**
  - 모든 화면의 레이아웃, 색상, 크기를 Figma 디자인에 맞게 코드에 반영
  - Theme 색상 추가 (surfaceLight, mapBackground, borderGray)
  - Button, Card 컴포넌트 스타일 수정
- ✅ TypeScript 오류 수정 완료
- ✅ Android 빌드 성공 (compileSdkVersion 34)
- ⚠️ 앱 로드 문제: Metro Bundler 연결 문제로 인해 앱이 JavaScript 번들을 로드하지 못함

### 진행 중 🚧

- 🚧 프론트엔드 앱 로드 문제 해결 (Metro Bundler 연결)
- 🚧 RunningScreen 완전 연동 (GPS 추적 구현 필요)
- 🚧 코스 생성 알고리즘 구현

### 다음 단계

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

자세한 진행 상황은 `DEVELOPMENT_CHECKLIST.md` 참고.

## 참고 자료

- [SRS 문서](plan/SRS_Running_App.md)
- [SDS 문서](plan/SDS_Running_App.md)
- [API 명세서](plan/api-specification.yaml)
- [기술 스택 결정](plan/SRS_Technology_Decisions.md)
- [코스 생성 알고리즘](plan/distance_constrained_loop_v1_0.md)
- [프론트엔드 아키텍처](plan/Frontend_Architecture_Design.md)
