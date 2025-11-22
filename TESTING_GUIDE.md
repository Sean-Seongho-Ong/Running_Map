# 테스트 환경 구성 가이드

이 문서는 Running Map 애플리케이션의 테스트 환경 구성 및 테스트 방법을 안내합니다.

## 목차

1. [환경 설정](#환경-설정)
2. [데이터베이스 초기화](#데이터베이스-초기화)
3. [샘플 데이터 삽입](#샘플-데이터-삽입)
4. [백엔드 서버 실행](#백엔드-서버-실행)
5. [프론트엔드 연결 테스트](#프론트엔드-연결-테스트)
6. [전체 플로우 테스트](#전체-플로우-테스트)

## 환경 설정

### 1. Conda 가상환경 활성화

```bash
conda activate running_map
```

### 2. Docker Compose 실행

PostgreSQL과 Redis를 실행합니다:

```bash
docker-compose up -d postgres redis
```

서비스 상태 확인:

```bash
docker-compose ps
```

### 3. 환경 변수 확인

백엔드 `.env` 파일이 올바르게 설정되어 있는지 확인:

- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_NAME=runningmap`
- `DB_USER=runningmap`
- `DB_PASSWORD=runningmap_dev`
- `REDIS_HOST=localhost`
- `REDIS_PORT=6379`

## 데이터베이스 초기화

### 1. 마이그레이션 적용

```bash
cd backend
alembic upgrade head
```

### 2. 데이터베이스 연결 확인

```bash
# PostgreSQL 연결 테스트
docker-compose exec postgres psql -U runningmap -d runningmap -c "SELECT version();"

# Redis 연결 테스트
docker-compose exec redis redis-cli ping
```

## 샘플 데이터 삽입

### 1. 스크립트 실행

테스트용 샘플 코스 데이터를 삽입합니다:

```bash
cd backend
python scripts/seed_test_data.py
```

### 2. 기존 데이터 삭제 후 삽입

기존 데이터를 모두 삭제하고 새로 삽입하려면:

```bash
python scripts/seed_test_data.py --clear
```

### 3. 삽입된 데이터 확인

```bash
# PostgreSQL에서 직접 확인
docker-compose exec postgres psql -U runningmap -d runningmap -c "SELECT name, distance FROM courses;"
```

또는 백엔드 API를 통해 확인:

```bash
curl http://localhost:8000/api/v1/courses
```

## 백엔드 서버 실행

### 1. 서버 시작

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. API 문서 확인

브라우저에서 다음 URL 접속:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. 헬스 체크 (선택사항)

서버가 정상 작동하는지 확인:

```bash
curl http://localhost:8000/health
```

## 프론트엔드 연결 테스트

### 1. API Base URL 설정 확인

`mobile/src/config.ts` 파일에서 API Base URL이 올바르게 설정되어 있는지 확인:

```typescript
// 개발 환경 (로컬)
const API_URL = 'http://localhost:8000/api/v1';

// Android 에뮬레이터
// const API_URL = 'http://10.0.2.2:8000/api/v1';
```

### 2. 네트워크 보안 설정 확인

Android 앱의 경우 `mobile/android/app/src/main/res/xml/network_security_config.xml`이 올바르게 설정되어 있는지 확인합니다.

### 3. CORS 설정 확인

백엔드 `main.py`에서 CORS 설정이 프론트엔드 도메인을 허용하는지 확인합니다.

### 4. 연결 테스트

프론트엔드 앱을 실행하고 다음을 확인:

1. 코스 목록 조회 (`GET /api/v1/courses`)
2. 코스 생성 (`POST /api/v1/courses/generate`)
3. 코스 저장 (`POST /api/v1/courses`)

## 전체 플로우 테스트

### 테스트 체크리스트

- [x] Docker Compose 실행 (PostgreSQL, Redis) ✅ 완료
- [x] 데이터베이스 마이그레이션 적용 ✅ 완료
- [x] 샘플 데이터 삽입 ✅ 완료 (9개 코스)
- [x] 백엔드 서버 실행 ✅ 완료
- [ ] API 문서 접근 확인
- [ ] 프론트엔드에서 코스 목록 조회 테스트
- [ ] 프론트엔드에서 코스 생성 테스트
- [ ] 프론트엔드에서 코스 저장 테스트
- [ ] 코스 상세 정보 표시 확인
- [ ] 코스 미리보기 기능 확인

### 현재 진행 상태 (2025-11-22)

#### 완료된 작업

1. **환경 설정**
   - ✅ Conda 가상환경 `running_map` 활성화
   - ✅ Docker Compose로 PostgreSQL, Redis 실행

2. **데이터베이스 초기화**
   - ✅ Alembic 마이그레이션 적용 완료
   - ✅ 데이터베이스 테이블 생성 확인

3. **샘플 데이터 삽입**
   - ✅ `backend/scripts/seed_test_data.py` 실행 완료
   - ✅ 총 9개 코스 성공적으로 삽입:
     - 서울 한강공원: 3km, 5km, 10km
     - 부산 해운대: 3km, 5km
     - 제주시: 5km, 10km
     - 대전 유성구: 3km, 5km
   - ✅ 모든 코스가 MockLoopGenerator를 사용하여 생성됨
   - ⚠️ 참고: Redis 캐시 저장 시 UUID 직렬화 경고 발생 (기능에는 영향 없음)

4. **백엔드 서버**
   - ✅ FastAPI 서버 실행 중
   - ✅ 서버 주소: http://localhost:8000
   - ✅ API 문서: http://localhost:8000/docs
   - ✅ 헬스 체크: http://localhost:8000/health

#### 실행된 명령어

```bash
# 1. 가상환경 활성화
conda activate running_map

# 2. 데이터베이스 마이그레이션
cd backend
alembic upgrade head

# 3. 샘플 데이터 삽입
python scripts/seed_test_data.py

# 4. 백엔드 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 다음 단계

1. **API 문서 확인**
   - 브라우저에서 http://localhost:8000/docs 접속
   - API 엔드포인트 목록 확인

2. **프론트엔드 테스트**
   - Android Studio에서 앱 실행
   - 코스 목록 조회 테스트
   - 코스 생성 및 저장 테스트

### 테스트 시나리오

#### 1. 코스 목록 조회

1. 프론트엔드 앱 실행
2. "내 코스" 화면으로 이동
3. 저장된 코스 목록이 표시되는지 확인
4. 샘플 데이터(서울, 부산, 제주 등)가 표시되는지 확인

#### 2. 코스 생성

1. "코스 생성" 화면으로 이동
2. 목표 거리 입력 (예: 5km)
3. "코스 생성" 버튼 클릭
4. 생성된 코스가 지도에 표시되는지 확인
5. 코스 상세 정보(거리, 오차, 알고리즘 등)가 표시되는지 확인

#### 3. 코스 저장

1. 생성된 코스에서 "이 코스 사용" 버튼 클릭
2. 코스 이름 입력
3. 코스가 저장되는지 확인
4. "내 코스" 목록에 새로 저장된 코스가 나타나는지 확인

#### 4. 코스 재생성

1. 생성된 코스에서 "다시 생성" 버튼 클릭
2. 동일한 파라미터로 새로운 코스가 생성되는지 확인
3. 코스 상세 정보가 업데이트되는지 확인

## 문제 해결

### 데이터베이스 연결 오류

```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose ps postgres

# 로그 확인
docker-compose logs postgres

# 컨테이너 재시작
docker-compose restart postgres
```

### Redis 연결 오류

```bash
# Redis 컨테이너 상태 확인
docker-compose ps redis

# 로그 확인
docker-compose logs redis

# 컨테이너 재시작
docker-compose restart redis
```

### 백엔드 서버 오류

```bash
# 포트 사용 확인
netstat -ano | findstr :8000

# 환경 변수 확인
cd backend
python -c "from config import settings; print(settings.database_url)"
```

### 프론트엔드 연결 오류

1. 백엔드 서버가 실행 중인지 확인
2. API Base URL이 올바른지 확인
3. Android 에뮬레이터의 경우 `10.0.2.2` 사용
4. 네트워크 보안 설정 확인
5. CORS 설정 확인

## 참고 사항

- MockLoopGenerator를 사용하여 더미 코스를 생성합니다
- 실제 알고리즘 구현 전까지 테스트용으로 사용됩니다
- 샘플 데이터는 다양한 위치와 거리 조합으로 구성됩니다
- 데이터베이스에 저장된 코스는 실제 PostGIS 형식으로 저장됩니다

## 현재 환경 정보

### 서버 정보
- **백엔드 서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **헬스 체크**: http://localhost:8000/health

### 데이터베이스 정보
- **PostgreSQL**: localhost:5432
- **데이터베이스명**: runningmap
- **사용자**: runningmap
- **Redis**: localhost:6379

### 샘플 데이터
현재 데이터베이스에 저장된 코스:
- 서울 한강공원 3km (ID: 9a37f472-9606-4463-9527-593492237884)
- 서울 한강공원 5km (ID: ca201f1d-ca53-41a6-a0bc-370403b44112)
- 서울 한강공원 10km (ID: 4bea7ac6-a114-4040-b109-d36f27983a0a)
- 부산 해운대 3km (ID: 0062f31a-a979-4bd6-a5fd-ce14e528631e)
- 부산 해운대 5km (ID: 52ed96fb-1987-4063-943e-fbcd5d5bd4e6)
- 제주시 5km (ID: afc55056-3050-43dc-add1-3c643383a522)
- 제주시 10km (ID: d7b75e95-8e1e-4f56-baa6-826b1e942bf2)
- 대전 유성구 3km (ID: c393fb78-c342-4f1e-a5f3-4baf0b61111c)
- 대전 유성구 5km (ID: e1bbac37-d87a-4697-8748-889e8c707ae7)

### 알려진 이슈
- Redis 캐시 저장 시 UUID 직렬화 경고: 기능에는 영향 없으나, 향후 수정 예정

