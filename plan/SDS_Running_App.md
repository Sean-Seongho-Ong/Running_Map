# Software Design Specification (SDS)
## 러닝 코스 자동 생성 및 추적 모바일 애플리케이션

**문서 버전:** 1.0  
**작성일:** 2024  
**프로젝트명:** Running Map App  
**참고 문서:** SRS_Running_App.md, distance_constrained_loop_v1_0.md

---

## 1. 소개 (Introduction)

### 1.1 목적 (Purpose)
이 문서는 러닝 코스 자동 생성 및 추적 모바일 애플리케이션의 상세 설계 사양을 정의합니다. SRS에서 정의된 요구사항을 바탕으로 시스템 아키텍처, 모듈 설계, 데이터베이스 스키마, API 설계 등을 상세히 기술합니다.

### 1.2 범위 (Scope)
이 문서는 다음을 포함합니다:
- 시스템 아키텍처 설계 (Clean Architecture 기반)
- 모듈별 상세 설계
- 데이터베이스 스키마 설계
- RESTful API 설계
- 주요 클래스 및 인터페이스 설계
- 코스 생성 알고리즘 모듈 상세 설계
- 러닝 추적 모듈 설계
- 배포 아키텍처

### 1.3 정의, 약어, 약칭
- **SDS**: Software Design Specification
- **Clean Architecture**: 계층형 아키텍처 패턴
- **Domain**: 비즈니스 로직 계층
- **Application**: 유즈케이스 계층
- **Infrastructure**: 인프라스트럭처 계층
- **Interface**: 인터페이스 계층 (API, UI)

### 1.4 참고 자료
- SRS_Running_App.md
- Distance-Constrained Loop Generation Algorithm v1.0
- Clean Architecture 원칙
- .cursor/rules/architecture.mdc (코딩 규칙)

---

## 2. 시스템 아키텍처 (System Architecture)

### 2.1 전체 아키텍처 개요

시스템은 Clean Architecture 원칙을 따라 계층형 구조로 설계됩니다.

```
┌─────────────────────────────────────────────────────────┐
│                    Mobile App (React Native)             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   UI Layer   │  │  State Mgmt  │  │  Services    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                          │ HTTPS (RESTful API)
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Backend Server (Python + FastAPI)           │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Interface Layer (API)                  │  │
│  │  - RESTful API Endpoints                          │  │
│  │  - Request/Response Validation                    │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │         Application Layer (Use Cases)             │  │
│  │  - Course Generation Service                      │  │
│  │  - Running Tracking Service                       │  │
│  │  - Course Management Service                      │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Domain Layer (Business Logic)           │  │
│  │  - Loop Generation Algorithm                      │  │
│  │  - Distance Calculation                           │  │
│  │  - Route Optimization                             │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                              │
│  ┌──────────────────────────────────────────────────┐  │
│  │      Infrastructure Layer (External Services)    │  │
│  │  - OSRM Client                                    │  │
│  │  - Database Repository                           │  │
│  │  - Redis Cache                                    │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │  │    Redis     │  │    OSRM      │
│ + PostGIS    │  │   (Cache)    │  │   (Routing)  │
└──────────────┘  └──────────────┘  └──────────────┘
```

### 2.2 아키텍처 원칙

1. **의존성 방향**: Interface → Application → Domain
2. **Domain 독립성**: Domain 계층은 외부 라이브러리나 프레임워크에 의존하지 않음
3. **인터페이스 추상화**: Infrastructure는 인터페이스를 통해 Application에 연결
4. **단일 책임 원칙**: 각 계층과 모듈은 명확한 책임을 가짐

### 2.3 기술 스택 (최종 결정)

**모바일 앱:**
- React Native (TypeScript)
- react-native-maps (OSM 타일 사용)
- @react-native-community/geolocation
- @react-navigation/native
- zustand (상태 관리)

**백엔드:**
- Python 3.11+
- FastAPI
- SQLAlchemy (ORM)
- GeoPy, Shapely (지리 데이터)
- numpy, scipy (수학 계산)
- httpx (비동기 HTTP)

**데이터베이스:**
- PostgreSQL 14+
- PostGIS 3.3+

**캐싱:**
- Redis 7+

**외부 서비스:**
- OSRM (라우팅)
- TileServer GL (지도 타일)

---

## 3. 모듈 설계 (Module Design)

### 3.1 백엔드 모듈 구조

```
backend/
├── domain/                    # 비즈니스 로직 (순수 Python) ✅ 구현 완료
│   ├── entities/              # 도메인 엔티티
│   │   ├── course.py          # 코스 엔티티
│   │   ├── route.py           # 경로 엔티티
│   │   └── running_session.py # 러닝 세션 엔티티
│   ├── value_objects/         # 값 객체
│   │   ├── coordinate.py      # 좌표 (lat, lon)
│   │   └── distance.py        # 거리
│   ├── services/              # 도메인 서비스 인터페이스
│   │   ├── loop_generator.py  # 루프 생성 알고리즘 인터페이스
│   │   ├── route_calculator.py # 경로 계산 인터페이스
│   │   └── distance_calculator.py # 거리 계산 (Haversine 구현 포함)
│   └── repositories/          # 리포지토리 인터페이스
│       ├── course_repository.py
│       └── running_session_repository.py
│
├── application/               # 유즈케이스 (구현 완료) ✅
│   ├── use_cases/
│   │   ├── generate_course.py      # 코스 생성 유즈케이스
│   │   ├── save_course.py         # 코스 저장 유즈케이스
│   │   ├── list_courses.py         # 코스 목록 조회 유즈케이스
│   │   ├── get_course.py           # 코스 상세 조회 유즈케이스
│   │   ├── delete_course.py        # 코스 삭제 유즈케이스
│   │   ├── start_running.py       # 러닝 시작 유즈케이스
│   │   ├── update_running.py       # 러닝 업데이트 유즈케이스
│   │   ├── update_location.py     # 위치 업데이트 유즈케이스
│   │   └── finish_running.py       # 러닝 종료 유즈케이스
│   └── dto/                   # 데이터 전송 객체
│       ├── course_dto.py
│       └── running_dto.py
│
├── infrastructure/            # 인프라스트럭처 (구현 완료) ✅
│   ├── database/
│   │   ├── models.py          # SQLAlchemy 모델
│   │   ├── session.py          # 데이터베이스 세션 관리
│   │   └── repositories/      # 리포지토리 구현
│   ├── external/
│   │   ├── osrm_client.py    # OSRM 클라이언트
│   │   └── tile_server_client.py # 타일 서버 클라이언트
│   ├── cache/
│   │   ├── redis_cache.py    # Redis 캐시 구현
│   │   └── course_cache.py    # 코스 캐싱 서비스
│   └── config/
│       └── settings.py        # 설정 관리 (재export)
│
├── interface/                 # API 인터페이스 (구현 완료) ✅
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── courses.py    # 코스 관련 API
│   │   │   │   ├── running.py    # 러닝 추적 API
│   │   │   │   └── users.py      # 사용자 API (향후)
│   │   │   └── dependencies.py  # 의존성 주입
│   │   └── middleware/        # 미들웨어
│   │       ├── auth.py
│   │       └── error_handler.py
│   └── schemas/               # Pydantic 스키마
│       ├── course_schema.py
│       └── running_schema.py
│
├── alembic/                   # 데이터베이스 마이그레이션 ✅
│   ├── env.py
│   └── script.py.mako
│
├── main.py                    # FastAPI 앱 진입점 ✅
├── config.py                  # 환경 변수 설정 ✅
├── alembic.ini                # Alembic 설정 ✅
├── requirements.txt           # Python 의존성 ✅
└── environment.yml            # Conda 환경 설정 ✅
```

### 3.2 모바일 앱 모듈 구조 (Expo Bare Workflow)

**프로젝트 초기화:**
```bash
npx create-expo-app@latest RunningMapApp --template bare
```

**프로젝트 구조:**
```
mobile/
├── app.json                    # Expo 설정
├── package.json
├── tsconfig.json
├── ios/                        # iOS 네이티브 코드 (Expo Bare)
│   ├── Podfile
│   └── RunningMapApp/
├── android/                     # Android 네이티브 코드 (Expo Bare)
│   └── app/
├── src/
│   ├── domain/                # 비즈니스 로직
│   │   ├── entities/
│   │   │   ├── Course.ts
│   │   │   ├── RunningSession.ts
│   │   │   └── Location.ts
│   │   ├── valueObjects/
│   │   │   ├── Coordinate.ts
│   │   │   ├── Distance.ts
│   │   │   └── Pace.ts
│   │   └── services/
│   │       ├── CourseService.ts
│   │       └── RunningService.ts
│   │
│   ├── application/           # 유즈케이스
│   │   ├── useCases/
│   │   │   ├── GenerateCourseUseCase.ts
│   │   │   ├── SaveCourseUseCase.ts
│   │   │   └── TrackRunningUseCase.ts
│   │   └── repositories/
│   │       ├── CourseRepository.ts
│   │       └── ApiRepository.ts
│   │
│   ├── infrastructure/        # 인프라스트럭처
│   │   ├── api/
│   │   │   ├── apiClient.ts  # API 클라이언트
│   │   │   └── endpoints.ts
│   │   ├── storage/
│   │   │   └── AsyncStorage.ts # 로컬 저장소
│   │   └── location/
│   │       └── LocationService.ts # GPS 서비스
│   │
│   ├── interface/             # UI 계층
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
│   │   │   ├── useLocation.ts
│   │   │   ├── useCourseGeneration.ts
│   │   │   └── useRunningTracker.ts
│   │   └── store/             # 상태 관리
│   │       ├── courseStore.ts
│   │       ├── runningStore.ts
│   │       └── locationStore.ts
│   │
│   └── theme/                  # 디자인 시스템
│       ├── colors.ts
│       ├── typography.ts
│       ├── spacing.ts
│       └── index.ts
│
├── App.tsx                     # 앱 진입점
└── assets/
    ├── images/
    └── icons/
```

**Expo Bare Workflow 특징:**
- `ios/` 및 `android/` 폴더에 네이티브 코드 직접 관리
- `react-native-maps` 등 네이티브 모듈 완전 지원
- Expo Dev Client로 빠른 개발 및 테스트
- OTA 업데이트 지원 (JavaScript 번들만)

---

## 4. 데이터베이스 스키마 설계

### 4.1 ERD 개요

```
┌──────────────┐         ┌──────────────┐
│    Users     │         │    Courses   │
├──────────────┤         ├──────────────┤
│ id (PK)      │◄──┐     │ id (PK)      │
│ email        │   │     │ user_id (FK) │
│ name         │   │     │ name         │
│ created_at   │   │     │ distance     │
└──────────────┘   │     │ polyline     │
                   │     │ metadata     │
                   │     │ created_at   │
                   │     │ is_public    │
                   │     └──────────────┘
                   │
┌──────────────┐   │
│RunningSessions│   │
├──────────────┤   │
│ id (PK)      │   │
│ user_id (FK) │───┘
│ course_id(FK)│───┐
│ start_time   │   │
│ end_time     │   │
│ total_distance│  │
│ avg_pace     │   │
│ elevation_gain│   │
│ route_polyline│   │
└──────────────┘   │
                   │
┌──────────────┐   │
│RunningSegments│  │
├──────────────┤   │
│ id (PK)      │   │
│ session_id(FK)──┘
│ segment_index│
│ distance     │
│ duration     │
│ pace         │
│ elevation    │
└──────────────┘
```

### 4.2 테이블 상세 설계

#### 4.2.1 users 테이블

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

#### 4.2.2 courses 테이블

```sql
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    distance DECIMAL(10, 2) NOT NULL, -- km
    polyline GEOMETRY(LINESTRING, 4326) NOT NULL, -- PostGIS
    metadata JSONB, -- 추가 메타데이터
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_public BOOLEAN DEFAULT FALSE,
    
    -- 공간 인덱스
    CONSTRAINT valid_polyline CHECK (ST_IsValid(polyline))
);

-- 공간 인덱스 (GIST)
CREATE INDEX idx_courses_polyline ON courses USING GIST(polyline);

-- 사용자별 인덱스
CREATE INDEX idx_courses_user_id ON courses(user_id);

-- 공개 코스 인덱스
CREATE INDEX idx_courses_public ON courses(is_public) WHERE is_public = TRUE;

-- 거리 범위 검색을 위한 인덱스
CREATE INDEX idx_courses_distance ON courses(distance);
```

#### 4.2.3 running_sessions 테이블

```sql
CREATE TABLE running_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id UUID REFERENCES courses(id) ON DELETE SET NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    total_distance DECIMAL(10, 2), -- km
    total_duration INTEGER, -- 초 단위
    avg_pace DECIMAL(5, 2), -- 분/km
    elevation_gain DECIMAL(8, 2), -- m
    route_polyline GEOMETRY(LINESTRING, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_running_sessions_user_id ON running_sessions(user_id);
CREATE INDEX idx_running_sessions_course_id ON running_sessions(course_id);
CREATE INDEX idx_running_sessions_start_time ON running_sessions(start_time);
CREATE INDEX idx_running_sessions_route ON running_sessions USING GIST(route_polyline);
```

#### 4.2.4 running_segments 테이블

```sql
CREATE TABLE running_segments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES running_sessions(id) ON DELETE CASCADE,
    segment_index INTEGER NOT NULL,
    distance DECIMAL(10, 2) NOT NULL, -- km
    duration INTEGER NOT NULL, -- 초 단위
    pace DECIMAL(5, 2), -- 분/km
    elevation DECIMAL(8, 2), -- m
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(session_id, segment_index)
);

CREATE INDEX idx_running_segments_session_id ON running_segments(session_id);
```

### 4.3 공간 쿼리 예시

#### 반경 내 코스 검색
```sql
-- 사용자 위치 기준 5km 반경 내 공개 코스 검색
SELECT 
    id, 
    name, 
    distance,
    ST_AsGeoJSON(polyline) as polyline_geojson
FROM courses
WHERE is_public = TRUE
  AND ST_DWithin(
    polyline::geography,
    ST_MakePoint(경도, 위도)::geography,
    5000  -- 5km (미터 단위)
  )
ORDER BY distance;
```

#### 코스 거리 계산
```sql
-- 코스의 실제 거리 계산 (PostGIS)
SELECT 
    id,
    name,
    ST_Length(polyline::geography) / 1000 as actual_distance_km
FROM courses
WHERE id = 'course-uuid';
```

---

## 5. API 설계 (RESTful API)

### 5.1 API 기본 정보

- **Base URL**: `https://api.runningmap.app/v1`
- **인증**: JWT Bearer Token (향후 구현)
- **응답 형식**: JSON
- **에러 처리**: 표준 HTTP 상태 코드

### 5.2 API 엔드포인트

#### 5.2.1 코스 생성 API

**POST** `/courses/generate`

**요청:**
```json
{
  "start_point": {
    "latitude": 37.5665,
    "longitude": 126.9780
  },
  "target_distance": 10.0,
  "parameters": {
    "step_init": 1.0,
    "tolerance_ratio": 0.1,
    "max_iter": 5
  }
}
```

**응답 (성공):**
```json
{
  "status": "OK",
  "course": {
    "id": "uuid",
    "polyline": [
      {"lat": 37.5665, "lon": 126.9780},
      {"lat": 37.5670, "lon": 126.9785},
      ...
    ],
    "distance": 10.2,
    "relative_error": 0.02,
    "algorithm": "STEP_ADAPTIVE",
    "iterations": 3,
    "step_used": 0.9,
    "metadata": {
      "estimated_time": 60,
      "elevation_gain": 150
    }
  }
}
```

**응답 (실패):**
```json
{
  "status": "FAIL",
  "error": {
    "code": "COURSE_GENERATION_FAILED",
    "message": "Unable to generate course within tolerance",
    "details": {
      "algorithm": "STEP_ADAPTIVE",
      "best_relative_error": 0.15
    }
  }
}
```

#### 5.2.2 코스 저장 API

**POST** `/courses`

**요청:**
```json
{
  "name": "한강 러닝 코스",
  "polyline": [
    {"lat": 37.5665, "lon": 126.9780},
    ...
  ],
  "distance": 10.2,
  "is_public": false,
  "metadata": {
    "tags": ["한강", "평지"],
    "difficulty": "easy"
  }
}
```

**응답:**
```json
{
  "id": "course-uuid",
  "name": "한강 러닝 코스",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 5.2.3 코스 목록 조회 API

**GET** `/courses?user_id={uuid}&public=true&limit=20&offset=0`

**응답:**
```json
{
  "courses": [
    {
      "id": "uuid",
      "name": "코스 이름",
      "distance": 10.0,
      "created_at": "2024-01-01T00:00:00Z",
      "is_public": true,
      "user_name": "사용자 이름"
    }
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### 5.2.4 코스 상세 조회 API

**GET** `/courses/{course_id}`

**응답:**
```json
{
  "id": "uuid",
  "name": "코스 이름",
  "distance": 10.0,
  "polyline": [
    {"lat": 37.5665, "lon": 126.9780},
    ...
  ],
  "metadata": {
    "elevation_gain": 150,
    "estimated_time": 60
  },
  "created_at": "2024-01-01T00:00:00Z",
  "user_id": "user-uuid"
}
```

#### 5.2.5 러닝 시작 API

**POST** `/running/start`

**요청:**
```json
{
  "course_id": "course-uuid",  // 선택사항
  "start_location": {
    "latitude": 37.5665,
    "longitude": 126.9780
  }
}
```

**응답:**
```json
{
  "session_id": "session-uuid",
  "started_at": "2024-01-01T12:00:00Z"
}
```

#### 5.2.6 러닝 위치 업데이트 API

**POST** `/running/{session_id}/location`

**요청:**
```json
{
  "location": {
    "latitude": 37.5665,
    "longitude": 126.9780,
    "altitude": 50.0,
    "timestamp": "2024-01-01T12:00:05Z"
  }
}
```

**응답:**
```json
{
  "session_id": "session-uuid",
  "current_stats": {
    "distance": 0.5,
    "duration": 300,
    "pace": 5.0,
    "elevation_gain": 10
  }
}
```

#### 5.2.7 러닝 종료 API

**POST** `/running/{session_id}/finish`

**요청:**
```json
{
  "end_location": {
    "latitude": 37.5665,
    "longitude": 126.9780
  },
  "route": [
    {"lat": 37.5665, "lon": 126.9780, "timestamp": "..."},
    ...
  ]
}
```

**응답:**
```json
{
  "session_id": "session-uuid",
  "summary": {
    "total_distance": 10.2,
    "total_duration": 3600,
    "avg_pace": 5.88,
    "elevation_gain": 150,
    "segments": [
      {
        "index": 1,
        "distance": 1.0,
        "duration": 360,
        "pace": 6.0
      }
    ]
  }
}
```

### 5.3 에러 응답 형식

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적 에러 메시지",
    "details": {}
  }
}
```

**주요 에러 코드:**
- `VALIDATION_ERROR`: 입력값 검증 실패
- `COURSE_GENERATION_FAILED`: 코스 생성 실패
- `ROUTING_SERVICE_ERROR`: 라우팅 서비스 오류
- `DATABASE_ERROR`: 데이터베이스 오류
- `NOT_FOUND`: 리소스를 찾을 수 없음
- `UNAUTHORIZED`: 인증 실패

---

## 6. 주요 클래스 및 인터페이스 설계

### 6.1 Domain Layer

#### 6.1.1 LoopGenerator (도메인 서비스)

```python
# domain/services/loop_generator.py

from abc import ABC, abstractmethod
from domain.entities.route import Route
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

class LoopGenerator(ABC):
    """루프 생성 알고리즘 인터페이스"""
    
    @abstractmethod
    def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: dict
    ) -> Route:
        """
        루프 생성
        
        Args:
            start_point: 시작점 좌표
            target_distance: 목표 거리
            parameters: 알고리즘 파라미터
            
        Returns:
            Route: 생성된 루프 경로
            
        Raises:
            LoopGenerationError: 루프 생성 실패 시
        """
        pass


class DistanceConstrainedLoopGenerator(LoopGenerator):
    """Distance-Constrained Loop Generation Algorithm v1.0 구현"""
    
    def __init__(
        self,
        routing_service: RoutingService,
        snap_service: SnapService
    ):
        self.routing_service = routing_service
        self.snap_service = snap_service
    
    def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: dict
    ) -> Route:
        # Step 기반 + Adaptive Step 알고리즘 구현
        # distance_constrained_loop_v1_0.md 참조
        pass
```

#### 6.1.2 Coordinate (값 객체)

```python
# domain/value_objects/coordinate.py

from dataclasses import dataclass
from typing import Final

@dataclass(frozen=True)
class Coordinate:
    """지리 좌표 값 객체 (WGS84)"""
    
    latitude: float  # 위도 [-90, 90]
    longitude: float  # 경도 [-180, 180]
    
    MIN_LATITUDE: Final = -90.0
    MAX_LATITUDE: Final = 90.0
    MIN_LONGITUDE: Final = -180.0
    MAX_LONGITUDE: Final = 180.0
    
    def __post_init__(self):
        if not (self.MIN_LATITUDE <= self.latitude <= self.MAX_LATITUDE):
            raise ValueError(f"Latitude must be between {self.MIN_LATITUDE} and {self.MAX_LATITUDE}")
        if not (self.MIN_LONGITUDE <= self.longitude <= self.MAX_LONGITUDE):
            raise ValueError(f"Longitude must be between {self.MIN_LONGITUDE} and {self.MAX_LONGITUDE}")
    
    def to_dict(self) -> dict:
        return {"lat": self.latitude, "lon": self.longitude}
    
    @classmethod
    def from_dict(cls, data: dict) -> "Coordinate":
        return cls(
            latitude=data["lat"],
            longitude=data["lon"]
        )
```

#### 6.1.3 Route (엔티티)

```python
# domain/entities/route.py

from dataclasses import dataclass
from typing import List
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance

@dataclass
class Route:
    """경로 엔티티"""
    
    coordinates: List[Coordinate]
    total_distance: Distance
    algorithm_used: str
    relative_error: float
    
    def calculate_distance(self) -> Distance:
        """Haversine 공식을 사용한 실제 거리 계산"""
        # 구현 생략
        pass
    
    def to_polyline(self) -> List[dict]:
        """폴리라인 형식으로 변환"""
        return [coord.to_dict() for coord in self.coordinates]
```

### 6.2 Application Layer

#### 6.2.1 GenerateCourseUseCase

```python
# application/use_cases/generate_course.py

from typing import Optional
from domain.services.loop_generator import LoopGenerator
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from application.dto.course_dto import CourseGenerationRequest, CourseGenerationResponse

class GenerateCourseUseCase:
    """코스 생성 유즈케이스"""
    
    def __init__(
        self,
        loop_generator: LoopGenerator,
        cache_service: CacheService
    ):
        self.loop_generator = loop_generator
        self.cache_service = cache_service
    
    async def execute(
        self,
        request: CourseGenerationRequest
    ) -> CourseGenerationResponse:
        """
        코스 생성 실행
        
        1. 캐시 확인 (동일 시작점 + 거리)
        2. 루프 생성 알고리즘 실행
        3. 결과 캐싱
        4. 응답 생성
        """
        # 캐시 키 생성
        cache_key = self._generate_cache_key(
            request.start_point,
            request.target_distance
        )
        
        # 캐시 확인
        cached_result = await self.cache_service.get(cache_key)
        if cached_result:
            return CourseGenerationResponse.from_cache(cached_result)
        
        # 루프 생성
        route = await self.loop_generator.generate(
            start_point=Coordinate.from_dict(request.start_point),
            target_distance=Distance(request.target_distance),
            parameters=request.parameters
        )
        
        # 결과 캐싱 (TTL: 24시간)
        await self.cache_service.set(
            cache_key,
            route.to_dict(),
            ttl=86400
        )
        
        # 응답 생성
        return CourseGenerationResponse.from_route(route)
    
    def _generate_cache_key(
        self,
        start_point: dict,
        target_distance: float
    ) -> str:
        """캐시 키 생성"""
        lat = round(start_point["lat"], 4)
        lon = round(start_point["lon"], 4)
        dist = round(target_distance, 1)
        return f"course:{lat}:{lon}:{dist}"
```

### 6.3 Infrastructure Layer

#### 6.3.1 OSRMClient

```python
# infrastructure/external/osrm_client.py

from typing import List, Optional
from domain.value_objects.coordinate import Coordinate
from infrastructure.config.settings import settings
import httpx

class OSRMClient:
    """OSRM 라우팅 서비스 클라이언트"""
    
    def __init__(self):
        self.base_url = settings.OSRM_BASE_URL
        self.timeout = settings.OSRM_TIMEOUT
        self.client = httpx.AsyncClient(timeout=self.timeout)
    
    async def route(
        self,
        coordinates: List[Coordinate],
        profile: str = "foot"  # foot, running
    ) -> dict:
        """
        경로 계산
        
        Args:
            coordinates: 좌표 리스트
            profile: 라우팅 프로파일 (foot, running)
            
        Returns:
            {
                "distance": 1234.5,  # 미터
                "duration": 900,  # 초
                "geometry": [...]  # 폴리라인
            }
        """
        coords_str = ";".join([
            f"{coord.longitude},{coord.latitude}"
            for coord in coordinates
        ])
        
        url = f"{self.base_url}/route/v1/{profile}/{coords_str}"
        params = {
            "overview": "full",
            "geometries": "geojson"
        }
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return self._parse_response(response.json())
        except httpx.HTTPError as e:
            raise RoutingServiceError(f"OSRM request failed: {e}")
    
    def _parse_response(self, data: dict) -> dict:
        """OSRM 응답 파싱"""
        if data.get("code") != "Ok":
            raise RoutingServiceError(f"OSRM error: {data.get('message')}")
        
        route = data["routes"][0]
        return {
            "distance": route["distance"],  # 미터
            "duration": route["duration"],  # 초
            "geometry": route["geometry"]["coordinates"]
        }
```

#### 6.3.2 CourseRepository (구현)

```python
# infrastructure/database/repositories/course_repository.py

from typing import List, Optional
from domain.entities.course import Course
from domain.repositories.course_repository import ICourseRepository
from infrastructure.database.models import CourseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CourseRepository(ICourseRepository):
    """코스 리포지토리 구현"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def save(self, course: Course) -> Course:
        """코스 저장"""
        model = CourseModel.from_domain(course)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()
    
    async def find_by_id(self, course_id: str) -> Optional[Course]:
        """ID로 코스 조회"""
        result = await self.session.execute(
            select(CourseModel).where(CourseModel.id == course_id)
        )
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None
    
    async def find_by_user(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Course]:
        """사용자별 코스 목록 조회"""
        result = await self.session.execute(
            select(CourseModel)
            .where(CourseModel.user_id == user_id)
            .limit(limit)
            .offset(offset)
        )
        models = result.scalars().all()
        return [model.to_domain() for model in models]
```

---

## 7. 코스 생성 알고리즘 모듈 상세 설계

### 7.1 알고리즘 모듈 구조

```
domain/services/loop_generator/
├── __init__.py
├── base.py                    # 기본 인터페이스
├── step_based.py              # Step 기반 알고리즘 (v0.2)
├── sp_based.py                # S-P 기반 알고리즘 (v0.1)
├── adaptive_step.py           # Adaptive Step (v0.3)
├── v1_0_generator.py         # 통합 알고리즘 (v1.0)
└── utils/
    ├── geometry.py            # 기하학적 계산
    ├── snap.py                # 도로 스냅
    └── scoring.py             # 품질 점수 계산
```

### 7.2 주요 클래스 설계

#### 7.2.1 StepBasedLoopGenerator

```python
# domain/services/loop_generator/step_based.py

from typing import List
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from domain.entities.route import Route

class StepBasedLoopGenerator:
    """Step 기반 원둘레 분할 루프 생성 (v0.2)"""
    
    def __init__(
        self,
        routing_service: RoutingService,
        snap_service: SnapService
    ):
        self.routing_service = routing_service
        self.snap_service = snap_service
    
    async def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        step: Distance
    ) -> Route:
        """
        Step 기반 루프 생성
        
        알고리즘:
        1. R = D / (2π) 계산
        2. N ≈ D / step 계산
        3. Δθ = step / R 계산
        4. 이상적인 포인트 Q 생성
        5. 각 Q를 도로로 스냅 → V
        6. V → V+1 라우팅
        7. 루프 닫기
        """
        # 1. 기하학적 계산
        radius = self._calculate_radius(target_distance)
        num_steps = int(target_distance.km / step.km)
        delta_theta = step.km / radius
        
        # 2. 이상적인 포인트 생성
        ideal_points = self._generate_ideal_points(
            start_point,
            radius,
            num_steps,
            delta_theta
        )
        
        # 3. 도로 스냅
        snapped_points = await self._snap_to_roads(ideal_points)
        
        # 4. 라우팅
        route_segments = await self._route_segments(snapped_points, start_point)
        
        # 5. 루프 구성
        return self._build_route(route_segments, target_distance)
    
    def _calculate_radius(self, distance: Distance) -> float:
        """이상적인 원 반지름 계산"""
        import math
        return distance.km / (2 * math.pi)
    
    def _generate_ideal_points(
        self,
        start: Coordinate,
        radius: float,
        num_steps: int,
        delta_theta: float
    ) -> List[Coordinate]:
        """이상적인 포인트 Q 생성"""
        from domain.services.loop_generator.utils.geometry import (
            calculate_point_at_distance_and_angle
        )
        
        points = [start]
        for i in range(1, num_steps):
            angle = i * delta_theta
            point = calculate_point_at_distance_and_angle(
                start,
                radius,
                angle
            )
            points.append(point)
        return points
    
    async def _snap_to_roads(
        self,
        ideal_points: List[Coordinate]
    ) -> List[Coordinate]:
        """도로로 스냅"""
        snapped = []
        for point in ideal_points:
            snapped_point = await self.snap_service.snap(
                point,
                search_radius=300  # 300m
            )
            if snapped_point:
                snapped.append(snapped_point)
            else:
                # 스냅 실패 시 원본 좌표 사용 (또는 스킵)
                snapped.append(point)
        return snapped
```

#### 7.2.2 AdaptiveStepController

```python
# domain/services/loop_generator/adaptive_step.py

from typing import Tuple, Optional
from domain.value_objects.distance import Distance
from domain.entities.route import Route

class AdaptiveStepController:
    """양방향 Adaptive Step 제어"""
    
    def __init__(
        self,
        step_init: float = 1.0,
        step_min: float = 0.4,
        step_max: float = 2.0,
        tolerance_ratio: float = 0.1,
        shrink_factor: float = 0.8,
        grow_factor: float = 1.2,
        max_iter: int = 5
    ):
        self.step_init = step_init
        self.step_min = step_min
        self.step_max = step_max
        self.tolerance_ratio = tolerance_ratio
        self.shrink_factor = shrink_factor
        self.grow_factor = grow_factor
        self.max_iter = max_iter
    
    def should_continue(
        self,
        current_route: Route,
        target_distance: Distance,
        iteration: int
    ) -> Tuple[bool, Optional[float]]:
        """
        반복 계속 여부 및 다음 step 값 결정
        
        Returns:
            (should_continue, next_step)
        """
        if iteration >= self.max_iter:
            return (False, None)
        
        error = abs(current_route.total_distance.km - target_distance.km)
        rel_error = error / target_distance.km
        
        # 허용 오차 내
        if rel_error <= self.tolerance_ratio:
            return (False, None)
        
        # step 조정
        current_step = getattr(current_route, 'step_used', self.step_init)
        
        if current_route.total_distance > target_distance:
            # 너무 김 → step 줄이기
            next_step = max(current_step * self.shrink_factor, self.step_min)
        else:
            # 너무 짧음 → step 늘리기
            next_step = min(current_step * self.grow_factor, self.step_max)
        
        # step이 변하지 않으면 종료
        if abs(next_step - current_step) < 0.01:
            return (False, None)
        
        return (True, next_step)
```

#### 7.2.3 V1_0LoopGenerator (통합)

```python
# domain/services/loop_generator/v1_0_generator.py

from domain.services.loop_generator.step_based import StepBasedLoopGenerator
from domain.services.loop_generator.sp_based import SPBasedLoopGenerator
from domain.services.loop_generator.adaptive_step import AdaptiveStepController

class V1_0LoopGenerator:
    """Distance-Constrained Loop Generation Algorithm v1.0"""
    
    def __init__(
        self,
        step_generator: StepBasedLoopGenerator,
        sp_generator: SPBasedLoopGenerator,
        adaptive_controller: AdaptiveStepController
    ):
        self.step_generator = step_generator
        self.sp_generator = sp_generator
        self.adaptive_controller = adaptive_controller
    
    async def generate(
        self,
        start_point: Coordinate,
        target_distance: Distance,
        parameters: dict
    ) -> Route:
        """
        v1.0 통합 알고리즘 실행
        
        전략:
        1. Step 기반 + Adaptive Step 시도
        2. 실패 시 S-P 기반 시도
        3. 최종 Fallback
        """
        # Phase 1: Step 기반 + Adaptive
        step_result = await self._try_step_based(
            start_point,
            target_distance,
            parameters
        )
        
        if step_result.status == "OK":
            return step_result
        
        # Phase 2: S-P 기반 Fallback
        if parameters.get("use_SP_fallback", True):
            sp_result = await self._try_sp_based(
                start_point,
                target_distance
            )
            
            # 결과 비교
            return self._choose_better_result(
                step_result,
                sp_result,
                target_distance
            )
        
        # Phase 3: 최종 Fallback
        return await self._final_fallback(
            start_point,
            target_distance
        )
```

---

## 8. 러닝 추적 모듈 설계

### 8.1 러닝 추적 서비스

```python
# domain/services/running_tracker.py

from typing import List
from domain.value_objects.coordinate import Coordinate
from domain.value_objects.distance import Distance
from domain.value_objects.pace import Pace

class RunningTracker:
    """러닝 추적 서비스"""
    
    def __init__(self):
        self.locations: List[Coordinate] = []
        self.timestamps: List[float] = []
    
    def add_location(
        self,
        coordinate: Coordinate,
        timestamp: float
    ):
        """위치 추가"""
        self.locations.append(coordinate)
        self.timestamps.append(timestamp)
    
    def calculate_current_distance(self) -> Distance:
        """현재까지 누적 거리 계산"""
        if len(self.locations) < 2:
            return Distance(0.0)
        
        total = 0.0
        for i in range(1, len(self.locations)):
            dist = self._haversine_distance(
                self.locations[i-1],
                self.locations[i]
            )
            total += dist
        
        return Distance(total)
    
    def calculate_current_pace(self) -> Optional[Pace]:
        """현재 페이스 계산 (분/km)"""
        if len(self.locations) < 2:
            return None
        
        distance = self.calculate_current_distance()
        duration = self.timestamps[-1] - self.timestamps[0]
        
        if distance.km == 0:
            return None
        
        pace_min_per_km = (duration / 60) / distance.km
        return Pace(pace_min_per_km)
    
    def calculate_elevation_gain(self) -> float:
        """누적 상승 고도 계산"""
        # 기압계 또는 고도 데이터 필요
        # 구현 생략
        pass
    
    def _haversine_distance(
        self,
        coord1: Coordinate,
        coord2: Coordinate
    ) -> float:
        """Haversine 공식으로 거리 계산 (km)"""
        from math import radians, sin, cos, sqrt, atan2
        
        R = 6371.0  # 지구 반지름 (km)
        
        lat1 = radians(coord1.latitude)
        lon1 = radians(coord1.longitude)
        lat2 = radians(coord2.latitude)
        lon2 = radians(coord2.longitude)
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        return R * c
```

---

## 9. 시퀀스 다이어그램

### 9.1 코스 생성 시퀀스

```
사용자          모바일 앱          API 서버          LoopGenerator      OSRM
  │                │                 │                    │              │
  │--거리 입력---->│                 │                    │              │
  │                │--POST /courses/generate------------>│              │
  │                │                 │                    │              │
  │                │                 │--generate()------->│              │
  │                │                 │                    │              │
  │                │                 │                    │--route()---->│
  │                │                 │                    │<--경로-------│
  │                │                 │                    │              │
  │                │                 │<--Route------------│              │
  │                │<--Course Response---------------------│              │
  │<--코스 표시----│                 │                    │              │
```

### 9.2 러닝 추적 시퀀스

```
사용자          모바일 앱          API 서버          RunningTracker    DB
  │                │                 │                    │              │
  │--러닝 시작---->│                 │                    │              │
  │                │--POST /running/start---------------->│              │
  │                │                 │--create_session()--│------------->│
  │                │<--session_id------------------------│<-------------│
  │                │                 │                    │              │
  │--GPS 업데이트->│                 │                    │              │
  │                │--POST /running/{id}/location------->│              │
  │                │                 │--update_location()│              │
  │                │                 │--calculate_stats()│              │
  │                │<--current_stats---------------------│              │
  │<--통계 표시----│                 │                    │              │
  │                │                 │                    │              │
  │--러닝 종료---->│                 │                    │              │
  │                │--POST /running/{id}/finish---------->│              │
  │                │                 │--save_session()---│------------->│
  │                │<--summary---------------------------│<-------------│
  │<--결과 표시----│                 │                    │              │
```

---

## 10. 배포 아키텍처

### 10.1 개발 환경 (로컬)

```
┌─────────────────────────────────────────┐
│         개발자 머신 (로컬)                │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  React Native App (개발 모드)     │  │
│  └──────────────────────────────────┘  │
│              │                          │
│              │ localhost:8000          │
│              ▼                          │
│  ┌──────────────────────────────────┐  │
│  │  Docker Compose                  │  │
│  │  ├── FastAPI (로컬 실행)          │  │
│  │  ├── PostgreSQL + PostGIS       │  │
│  │  ├── Redis                       │  │
│  │  ├── OSRM                        │  │
│  │  └── TileServer GL (선택)        │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 10.2 프로토타입 환경 (VPS)

```
┌─────────────────────────────────────────┐
│              VPS 서버                    │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Docker Compose                  │  │
│  │  ├── FastAPI (포트 8000)         │  │
│  │  ├── PostgreSQL + PostGIS       │  │
│  │  ├── Redis                       │  │
│  │  ├── OSRM                        │  │
│  │  └── TileServer GL               │  │
│  └──────────────────────────────────┘  │
│              │                          │
│              │ Nginx (리버스 프록시)    │
│              │ HTTPS (Let's Encrypt)   │
└─────────────────────────────────────────┘
              │
              │ HTTPS
              ▼
        모바일 앱 (프로덕션)
```

### 10.3 프로덕션 환경 (클라우드)

```
┌─────────────────────────────────────────┐
│           클라우드 (AWS/GCP)             │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Load Balancer                   │  │
│  └──────────────────────────────────┘  │
│              │                          │
│    ┌─────────┼─────────┐               │
│    ▼         ▼         ▼               │
│  ┌─────┐  ┌─────┐  ┌─────┐            │
│  │App  │  │App  │  │App  │            │
│  │Server│  │Server│  │Server│            │
│  └─────┘  └─────┘  └─────┘            │
│    │         │         │                │
│    └─────────┼─────────┘                │
│              ▼                          │
│  ┌──────────────────────────────────┐  │
│  │  Managed Services                │  │
│  │  ├── RDS (PostgreSQL + PostGIS)  │  │
│  │  ├── ElastiCache (Redis)         │  │
│  │  └── EC2 (OSRM, TileServer GL)   │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 10.4 Docker Compose 구성 (개발 환경)

```yaml
# docker-compose.yml

version: '3.8'

services:
  postgres:
    image: postgis/postgis:14-3.3
    environment:
      POSTGRES_DB: runningmap
      POSTGRES_USER: runningmap
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  osrm:
    image: osrm/osrm-backend:latest
    ports:
      - "5000:5000"
    volumes:
      - ./osrm-data:/data
    command: osrm-routed --algorithm mld /data/korea-latest.osrm

  tileserver:
    image: maptiler/tileserver-gl:latest
    ports:
      - "8080:80"
    volumes:
      - ./tiles:/data
    environment:
      - TILESET_FILE=/data/korea.mbtiles

volumes:
  postgres_data:
  redis_data:
```

---

## 11. 보안 설계

### 11.1 인증 및 인가

- **JWT 토큰 기반 인증** (향후 구현)
- **API 키 관리**: 환경 변수 또는 Keychain/Keystore
- **HTTPS 필수**: 모든 통신 암호화

### 11.2 데이터 보호

- **위치 정보 암호화**: 전송 시 HTTPS, 저장 시 선택적 암호화
- **개인정보 보호**: GDPR 및 개인정보보호법 준수
- **입력값 검증**: Pydantic 스키마를 통한 검증

### 11.3 API 보안

- **Rate Limiting**: API 호출 제한
- **CORS 설정**: 허용된 도메인만 접근
- **에러 메시지**: 민감 정보 노출 방지

---

## 12. 성능 최적화 전략

### 12.1 캐싱 전략

1. **코스 생성 결과 캐싱**
   - 키: `course:{lat}:{lon}:{distance}`
   - TTL: 24시간
   - Redis 저장

2. **라우팅 결과 캐싱**
   - 키: `route:{start_lat}:{start_lon}:{end_lat}:{end_lon}`
   - TTL: 7일
   - Redis 저장

3. **코스 목록 캐싱**
   - 키: `courses:user:{user_id}:page:{page}`
   - TTL: 5분
   - Redis 저장

### 12.2 데이터베이스 최적화

1. **인덱스 전략**
   - 공간 인덱스 (GIST) 활용
   - 사용자별 인덱스
   - 시간 기반 인덱스

2. **쿼리 최적화**
   - N+1 문제 방지 (Eager Loading)
   - 페이지네이션 필수
   - 필요한 컬럼만 선택

### 12.3 비동기 처리

- **코스 생성**: 백그라운드 태스크로 처리 (Celery 고려)
- **라우팅 요청**: 비동기 HTTP 클라이언트 사용
- **배치 처리**: 여러 라우팅 요청을 배치로 처리

---

## 13. 테스트 전략

### 13.1 단위 테스트

- **Domain Layer**: 순수 함수 테스트 (의존성 없음)
- **Application Layer**: Mock을 사용한 유즈케이스 테스트
- **Infrastructure Layer**: 통합 테스트 또는 테스트 더블

### 13.2 통합 테스트

- **API 테스트**: FastAPI TestClient 사용
- **데이터베이스 테스트**: 테스트 DB 사용
- **외부 서비스 테스트**: Mock 서버 사용

### 13.3 E2E 테스트

- **모바일 앱**: Detox 또는 Appium
- **전체 플로우**: 코스 생성부터 러닝 추적까지

---

## 14. 모니터링 및 로깅

### 14.1 로깅 전략

- **로깅 레벨**: DEBUG, INFO, WARN, ERROR, FATAL
- **로깅 포맷**: JSON (구조화된 로그)
- **Trace ID**: 요청 추적을 위한 고유 ID

### 14.2 모니터링

- **성능 모니터링**: API 응답 시간, 처리량
- **에러 모니터링**: 에러율, 에러 유형
- **리소스 모니터링**: CPU, 메모리, 디스크 사용량

---

## 15. 부록

### 15.1 주요 라이브러리 버전

**백엔드:**
- Python: 3.11+
- FastAPI: 0.104+
- SQLAlchemy: 2.0+
- GeoPy: 2.4+
- Shapely: 2.0+
- httpx: 0.25+

**모바일:**
- React Native: 0.72+
- react-native-maps: 1.8+
- TypeScript: 5.0+

**인프라:**
- PostgreSQL: 14+
- PostGIS: 3.3+
- Redis: 7+
- Docker: 24+

### 15.2 개발 환경 설정

**필수 도구:**
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- Git

**선택 도구:**
- VS Code / Cursor
- Postman (API 테스트)
- DBeaver (DB 관리)

---

**문서 끝**

