# 쿼리 최적화 가이드

이 문서는 리포지토리의 쿼리 최적화 기능 사용법을 설명합니다.

## 1. 필요한 필드만 선택하기

대량의 데이터를 조회할 때 필요한 필드만 선택하여 메모리 사용량을 줄일 수 있습니다.

### 사용 예시

```python
from infrastructure.database.repositories.course_repository import CourseRepositoryImpl

# 모든 필드 조회 (기본값)
course = await repository.get_by_id(course_id)

# 필요한 필드만 선택
course = await repository.get_by_id(
    course_id,
    select_fields=["id", "name", "distance", "is_public"]
)

# 목록 조회 시 필요한 필드만 선택
courses = await repository.list(
    is_public=True,
    limit=100,
    select_fields=["id", "name", "distance", "created_at"]
)
```

### 선택 가능한 필드

**CourseRepository:**
- `id`, `name`, `polyline`, `distance`, `metadata`, `is_public`, `user_id`, `created_at`, `updated_at`

**RunningSessionRepository:**
- `id`, `course_id`, `start_time`, `end_time`, `route_polyline`, `total_distance`, `total_duration`, `avg_pace`, `elevation_gain`

## 2. N+1 문제 방지 (Eager Loading)

관계가 있는 데이터를 조회할 때 N+1 문제를 방지하기 위해 eager loading을 사용할 수 있습니다.

### 현재 상태

현재는 관계(relationship)가 정의되지 않았지만, 향후 관계가 추가될 때를 대비하여 `load_relationships` 파라미터가 준비되어 있습니다.

### 향후 사용 예시

```python
# 관계가 추가된 후 사용 예시
# 예: CourseModel.running_sessions 관계가 추가된 경우

# Eager loading 사용
course = await repository.get_by_id(
    course_id,
    load_relationships=True  # running_sessions를 함께 로드
)

# 목록 조회 시에도 eager loading
courses = await repository.list(
    is_public=True,
    load_relationships=True
)
```

### 구현 세부사항

리포지토리 내부에서는 `selectinload`를 사용하여 관계를 로드합니다:

```python
from sqlalchemy.orm import selectinload

# 예시 (향후 관계 추가 시)
query = select(CourseModel).options(
    selectinload(CourseModel.running_sessions)
)
```

## 3. 인덱스 활용

다음 인덱스가 자동으로 활용됩니다:

### CourseModel 인덱스
- `idx_courses_polyline`: GIST 인덱스 (공간 검색)
- `idx_courses_user_id`: 사용자별 조회
- `idx_courses_public`: 공개 여부 필터링
- `idx_courses_distance`: 거리별 정렬

### RunningSessionModel 인덱스
- `idx_running_sessions_user_id`: 사용자별 조회
- `idx_running_sessions_course_id`: 코스별 조회
- `idx_running_sessions_start_time`: 시간별 정렬
- `idx_running_sessions_route`: GIST 인덱스 (공간 검색)

## 4. 성능 최적화 팁

### 1. 대량 데이터 조회 시

```python
# 나쁜 예: 모든 필드를 조회
courses = await repository.list(limit=1000)  # polyline 등 큰 데이터도 모두 로드

# 좋은 예: 필요한 필드만 선택
courses = await repository.list(
    limit=1000,
    select_fields=["id", "name", "distance", "created_at"]  # polyline 제외
)
```

### 2. 페이징 처리

```python
# LIMIT/OFFSET을 사용한 페이징
page_size = 20
page = 1

courses = await repository.list(
    is_public=True,
    limit=page_size,
    offset=(page - 1) * page_size
)
```

### 3. 관계 데이터가 필요한 경우

```python
# 관계가 추가된 후
# 나쁜 예: N+1 문제 발생
courses = await repository.list(is_public=True)
for course in courses:
    sessions = await session_repository.list(course_id=course.id)  # 각 코스마다 쿼리 실행

# 좋은 예: Eager loading 사용
courses = await repository.list(
    is_public=True,
    load_relationships=True  # running_sessions를 한 번에 로드
)
```

## 5. 성능 모니터링

성능 프로파일링 후 다음을 확인하세요:

1. **쿼리 실행 시간**: `EXPLAIN ANALYZE` 사용
2. **메모리 사용량**: 필요한 필드만 선택했을 때의 메모리 절감 효과
3. **N+1 문제**: 관계 데이터 조회 시 쿼리 개수 확인

## 참고사항

- `select_fields`를 사용할 때는 필수 필드(`id`, `name` 등)를 포함해야 합니다.
- `load_relationships`는 관계가 정의된 후에만 효과가 있습니다.
- 인덱스는 자동으로 활용되므로 별도 설정이 필요 없습니다.

