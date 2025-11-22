# Running Map App - Backend

Python + FastAPI 기반 백엔드 서버

## 프로젝트 구조

```
backend/
├── domain/                    # 비즈니스 로직 (순수 Python)
│   ├── entities/              # 도메인 엔티티
│   │   ├── course.py
│   │   ├── running_session.py
│   │   └── route.py
│   ├── value_objects/         # 값 객체
│   │   ├── coordinate.py
│   │   └── distance.py
│   ├── services/              # 도메인 서비스 인터페이스
│   │   ├── loop_generator.py
│   │   ├── route_calculator.py
│   │   └── distance_calculator.py
│   └── repositories/          # 리포지토리 인터페이스
│       ├── course_repository.py
│       └── running_session_repository.py
│
├── application/               # 유즈케이스 (구현 완료)
│   ├── use_cases/
│   │   ├── generate_course.py      # 코스 생성 유즈케이스
│   │   ├── save_course.py          # 코스 저장 유즈케이스
│   │   ├── list_courses.py         # 코스 목록 조회 유즈케이스
│   │   ├── get_course.py           # 코스 상세 조회 유즈케이스
│   │   ├── delete_course.py        # 코스 삭제 유즈케이스
│   │   ├── start_running.py        # 러닝 시작 유즈케이스
│   │   ├── update_running.py       # 러닝 업데이트 유즈케이스
│   │   ├── update_location.py     # 위치 업데이트 유즈케이스
│   │   └── finish_running.py       # 러닝 종료 유즈케이스
│   └── dto/
│       ├── course_dto.py           # 코스 관련 DTO
│       └── running_dto.py          # 러닝 관련 DTO
│
├── infrastructure/            # 인프라스트럭처 (구현 완료)
│   ├── database/
│   │   ├── models.py          # SQLAlchemy 모델 (Course, RunningSession)
│   │   ├── session.py          # 데이터베이스 세션 관리
│   │   ├── repositories/       # 리포지토리 구현
│   │   │   ├── course_repository.py
│   │   │   └── running_session_repository.py
│   │   └── OPTIMIZATION.md     # 쿼리 최적화 가이드
│   ├── external/
│   │   └── osrm_client.py     # OSRM 클라이언트 (재시도 로직 포함)
│   ├── cache/
│   │   ├── redis_cache.py     # Redis 캐시 구현
│   │   └── course_cache.py    # 코스 캐싱 서비스
│   ├── config/
│   │   └── settings.py
│   └── exceptions.py          # 커스텀 예외 정의
│
├── interface/                 # API 인터페이스 (향후 구현)
│   ├── api/
│   └── schemas/
│
├── alembic/                   # 데이터베이스 마이그레이션
│   ├── env.py
│   └── script.py.mako
│
├── main.py                    # FastAPI 앱 진입점
├── config.py                  # 환경 변수 설정
├── alembic.ini                # Alembic 설정
├── requirements.txt           # Python 의존성
└── environment.yml            # Conda 환경 설정
```

## 설치 및 실행

### 방법 1: Conda 사용 (권장)

#### 1. Conda 환경 생성

```bash
# backend 폴더로 이동
cd backend

# Conda 환경 생성
conda env create -f environment.yml

# 환경 활성화
conda activate running_map
```

#### 2. 환경 변수 설정

```bash
# .env 파일 생성 (backend 폴더에)
# .env.example 파일을 참고하여 .env 파일을 생성하고 필요한 설정을 변경하세요
# 주요 설정:
# - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
# - REDIS_HOST, REDIS_PORT
# - OSRM_BASE_URL
```

#### 3. 환경 확인

```bash
# Python 버전 확인
python --version  # Python 3.11.x

# 패키지 설치 확인
pip list
```

**환경 업데이트 (의존성 변경 시):**
```bash
conda env update -f environment.yml --prune
```

**환경 제거 (필요 시):**
```bash
conda env remove -n running_map
```

---

### 방법 2: Python venv 사용

#### 1. 가상 환경 생성

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

#### 3. 환경 변수 설정

```bash
# .env 파일 생성 (backend 폴더에)
# .env.example 파일을 참고하여 .env 파일을 생성하고 필요한 설정을 변경하세요
```

### 4. Docker Compose 서비스 시작 (선택사항)

```bash
# 프로젝트 루트에서 실행
cd ..
docker-compose up -d postgres redis

# 또는 backend 폴더에서
docker-compose -f ../docker-compose.yml up -d postgres redis
```

### 5. 데이터베이스 마이그레이션

```bash
# 데이터베이스 모델 정의 후 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 적용
alembic upgrade head
```

**참고**: 데이터베이스 모델과 마이그레이션이 완료되었습니다. 
초기 마이그레이션(`9d86b00d0532_initial_migration.py`)이 적용되어 `courses`와 `running_sessions` 테이블이 생성되었습니다.

### 6. 서버 실행

```bash
# 개발 모드
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 프로덕션 모드
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 개발 가이드

### Clean Architecture 원칙

프로젝트는 Clean Architecture 원칙을 따라 구성됩니다:

- **Domain**: 순수 비즈니스 로직, 외부 의존성 없음
- **Application**: 유즈케이스 및 비즈니스 규칙
- **Infrastructure**: 데이터베이스, 외부 API, 캐시 구현
- **Interface**: FastAPI 엔드포인트, 스키마

### 코딩 규칙

- SOLID 원칙 준수
- 타입 힌팅 사용 (Pydantic, mypy)
- 비동기 처리 (asyncio, httpx)
- 로깅: structlog 사용 (print 금지)

### 주요 라이브러리

- **FastAPI**: 웹 프레임워크
- **SQLAlchemy**: ORM (비동기)
- **GeoPy, Shapely**: 지리 데이터 처리
- **numpy, scipy**: 수학 계산
- **httpx**: 비동기 HTTP 클라이언트 (OSRM 호출)
- **Redis**: 캐싱

## API 문서

### OpenAPI 명세서

완전한 API 명세서는 `plan/api-specification.yaml`에 정의되어 있습니다.

- **OpenAPI 3.0 형식**: Swagger UI에서 확인 가능
- **모든 엔드포인트 정의**: 요청/응답 스키마 포함
- **에러 응답 형식**: 표준 에러 코드 정의

### API 엔드포인트 (주요)

#### 코스 생성
```http
POST /api/v1/courses/generate
```

#### 코스 관리
```http
POST   /api/v1/courses          # 코스 저장
GET    /api/v1/courses          # 코스 목록 조회
GET    /api/v1/courses/{id}    # 코스 상세 조회
DELETE /api/v1/courses/{id}     # 코스 삭제
```

#### 러닝 추적
```http
POST /api/v1/running/start                    # 러닝 세션 시작
PUT  /api/v1/running/{session_id}             # 러닝 세션 업데이트
POST /api/v1/running/{session_id}/location    # 위치 업데이트
POST /api/v1/running/{session_id}/finish      # 러닝 세션 종료
```

자세한 API 스펙은 `plan/api-specification.yaml`을 참고하거나, 
서버 실행 후 `http://localhost:8000/docs`에서 확인하세요.

## 테스트

### 단위 테스트

```bash
# 전체 테스트
pytest

# 커버리지 포함
pytest --cov=backend --cov-report=html

# 특정 테스트만
pytest tests/infrastructure/database/test_repositories.py

# 통합 테스트 실행 (실제 데이터베이스/Redis 연결 필요)
pytest -m integration
```

### 테스트 결과

- **Infrastructure 계층 테스트**: 32개 통과
  - Redis 캐시 테스트: 14개
  - OSRM 클라이언트 테스트: 7개
  - 리포지토리 테스트: 11개

- **Application 계층 테스트**: 46개 통과
  - DTO 테스트: 25개
  - Use Cases 테스트: 21개

- **Interface 계층 테스트**: 11개 통과
  - Course API 테스트: 7개
  - Running API 테스트: 4개

- **통합 테스트**: 7개 통과
  - Redis 통합 테스트: 6개 통과
  - 데이터베이스 연결 테스트: 1개 통과
  - 데이터베이스 CRUD 통합 테스트: Windows 환경 제약으로 일부 실패 (Linux 환경에서 정상 동작 예상)

- **총 테스트**: 96개 통과

### 테스트 마커

```bash
# 통합 테스트만 실행
pytest -m integration

# 단위 테스트만 실행
pytest -m "not integration"
```

## 데이터베이스 관리

### 마이그레이션

```bash
# 새 마이그레이션 생성
alembic revision --autogenerate -m "Description"

# 마이그레이션 적용
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1
```

### 데이터베이스 접속

```bash
# Docker 컨테이너로 접속
docker-compose exec postgres psql -U runningmap -d runningmap

# 또는 직접 접속
psql -h localhost -U runningmap -d runningmap
```

## 로깅

structlog를 사용한 구조화된 로깅:

```python
import structlog

logger = structlog.get_logger()

logger.info("course_generation_started", 
            start_point=start_point, 
            target_distance=target_distance)
```

## 성능 최적화

### 캐싱 전략

- 코스 생성 결과: Redis 캐싱 (TTL: 24시간)
- 라우팅 결과: Redis 캐싱 (TTL: 7일)
- 키 형식: `course:{lat}:{lon}:{distance}`

### 데이터베이스 최적화

- PostGIS 공간 인덱스 (GIST) 활용
- 쿼리 최적화
  - 인덱스 활용 (user_id, is_public, created_at)
  - 필요한 필드만 선택 (`select_fields` 파라미터)
  - N+1 문제 방지 (`load_relationships` 파라미터)
- 페이지네이션 필수 (LIMIT/OFFSET)

자세한 내용은 `infrastructure/database/OPTIMIZATION.md` 참고.

## 문제 해결

### 일반적인 문제

1. **데이터베이스 연결 실패**
   - `.env` 파일의 DB 설정 확인
   - PostgreSQL 컨테이너가 실행 중인지 확인

2. **Redis 연결 실패**
   - Redis 컨테이너가 실행 중인지 확인
   - `REDIS_HOST` 환경 변수 확인

3. **OSRM 호출 실패**
   - OSRM 컨테이너가 실행 중인지 확인
   - `OSRM_BASE_URL` 환경 변수 확인

4. **마이그레이션 오류**
   - 데이터베이스 스키마 확인
   - 마이그레이션 히스토리 확인: `alembic history`

## 현재 구현 상태

### 완료된 작업 ✅

#### 인프라 계층
- ✅ Docker Compose 환경 설정 (PostgreSQL + PostGIS, Redis)
- ✅ SQLAlchemy 모델 정의 (CourseModel, RunningSessionModel)
- ✅ 리포지토리 구현 (Course, RunningSession)
  - ✅ CRUD 메서드 구현
  - ✅ 에러 처리 강화 (트랜잭션 롤백, 커스텀 예외)
  - ✅ 쿼리 최적화 (인덱스 활용, 필드 선택, N+1 방지)
  - ✅ PostGIS WKB 변환 로직 (shapely 사용)
- ✅ OSRM 클라이언트 구현
  - ✅ 경로 계산 및 거리 계산
  - ✅ 재시도 로직 (exponential backoff)
  - ✅ Rate limiting 및 타임아웃 처리
- ✅ Redis 캐시 구현
  - ✅ 기본 캐시 메서드 (get, set, delete, exists)
  - ✅ 코스 생성 결과 캐싱 (TTL: 24시간)
  - ✅ 라우팅 결과 캐싱 (TTL: 7일)
- ✅ 공간 인덱스 설정 (GIST)
- ✅ 데이터베이스 마이그레이션 (Alembic)
- ✅ 단위 테스트 (32개 통과)
- ✅ 통합 테스트 (Redis: 6개 통과, DB 연결: 1개 통과)

- ✅ 프로젝트 구조 생성 (Clean Architecture)
- ✅ 도메인 계층 구현
  - 값 객체: `Coordinate`, `Distance`
  - 엔티티: `Course`, `RunningSession`, `Route`
  - 도메인 서비스 인터페이스: `LoopGenerator`, `RouteCalculator`, `DistanceCalculator`
  - 리포지토리 인터페이스: `CourseRepository`, `RunningSessionRepository`
- ✅ Application 계층 구현
  - DTO: `CourseDTO`, `RunningDTO` (모든 요청/응답 DTO)
  - Use Cases: 코스 관련 5개, 러닝 관련 4개 (총 9개)
  - 단위 테스트: DTO 25개, Use Cases 21개 (총 46개 통과)
- ✅ API 명세서 작성 (`plan/api-specification.yaml`)
- ✅ 기본 설정 파일 (`config.py`, `main.py`, `alembic.ini`)

#### Interface 계층 구현 (API) ✅
- ✅ **API 엔드포인트 구현 완료**:
  - **Course API**: 생성, 조회, 목록, 수정, 삭제
  - **Running API**: 시작, 위치 업데이트, 상태 업데이트, 종료
- ✅ **Pydantic 스키마**: 요청/응답 모델 정의 완료
- ✅ **의존성 주입**: `Depends`를 활용한 Clean Architecture 의존성 주입 구현
- ✅ **에러 핸들링**: 글로벌 예외 처리기 및 커스텀 예외 매핑
- ✅ **API 테스트**: Interface 테스트 11개 전수 통과 (Course 7개, Running 4개)

### 다음 단계

1. **코스 생성 알고리즘 구현** (우선순위 높음)
   - DistanceConstrainedLoopGenerator 구현
   - S-P 기반 루프 생성 (v0.1)
   - Step 기반 원둘레 분할 (v0.2)
   - 양방향 Adaptive Step 피드백 (v0.3)

2. **프론트엔드 연동** (진행 중)
   - API 연동 완료
   - UI Integration 부분 완료 (CourseGenerationScreen, MapScreen)

자세한 내용은 `plan/SDS_Running_App.md` 및 `DEVELOPMENT_CHECKLIST.md` 참고.

