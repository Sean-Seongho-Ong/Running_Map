# 기술 스택 선택 사항 검토 문서
## Running Map App - SRS 단계 결정 사항

**작성일:** 2024  
**목적:** SRS 문서에 명시된 여러 기술 옵션 중 최종 선택을 위한 검토 문서

---

## 1. 모바일 앱 개발 프레임워크

### 선택 사항

#### 옵션 1: React Native (TypeScript) ⭐ 권장
**장점:**
- 하나의 코드베이스로 안드로이드/iOS 동시 개발
- JavaScript/TypeScript 사용으로 개발 속도 빠름
- 풍부한 라이브러리 생태계
- 네이티브 모듈 연동 가능
- 지도 라이브러리 (`react-native-maps`) 성숙도 높음

**단점:**
- 성능이 네이티브보다 약간 낮을 수 있음
- 복잡한 지도 기능 구현 시 제약 가능

**추천 라이브러리:**
- 지도: `react-native-maps`
- 위치: `@react-native-community/geolocation`
- 네비게이션: `@react-navigation/native`
- 상태 관리: `zustand` 또는 `redux-toolkit`

**비용:** 무료 (오픈소스)

---

#### 옵션 2: Flutter (Dart)
**장점:**
- 하나의 코드베이스로 안드로이드/iOS 동시 개발
- 네이티브에 가까운 성능
- Material Design 및 Cupertino 위젯 제공
- Hot Reload로 개발 속도 빠름

**단점:**
- Dart 언어 학습 필요
- 라이브러리 생태계가 React Native보다 작음
- 지도 라이브러리 선택지 제한적

**추천 라이브러리:**
- 지도: `google_maps_flutter`, `flutter_map`
- 위치: `geolocator`

**비용:** 무료 (오픈소스)

---

#### 옵션 3: 네이티브 개발 (Kotlin + Swift)
**장점:**
- 최고의 성능
- 플랫폼별 최적화 가능
- 모든 기능 완전한 접근 가능
- 지도 SDK 완전 지원

**단점:**
- 두 개의 코드베이스 유지 필요
- 개발 시간 및 비용 증가 (약 2배)
- 유지보수 복잡도 증가
- 팀 인력 요구사항 증가

**비용:** 개발 시간 증가로 인한 간접 비용

---

### 결정 필요 사항
- [x] **선택:** React Native
- [x] **이유:** 지도 라이브러리 사용 가능

---

## 2. 백엔드 서버 프레임워크

### 선택 사항

#### 옵션 1: Python + FastAPI ⭐ 권장
**장점:**
- 거리 기반 루프 생성 알고리즘 구현 용이 (수학 라이브러리 풍부)
- 비동기 처리 지원 (asyncio)
- API 문서 자동 생성 (Swagger/OpenAPI)
- 지리 데이터 처리 라이브러리 풍부 (GeoPy, Shapely)
- 타입 힌팅 지원

**단점:**
- Python 런타임 성능이 Node.js보다 약간 낮을 수 있음

**추천 라이브러리:**
- 웹 프레임워크: `FastAPI`
- 지리 데이터: `GeoPy`, `Shapely`
- 수학 계산: `numpy`, `scipy`
- 비동기 HTTP: `httpx`
- ORM: `SQLAlchemy`

**비용:** 무료 (오픈소스)

**구현 전략:**
- **개발 단계**: 로컬 환경에서 FastAPI 서버 실행 (Docker Compose 사용)
- **프로토타입**: 로컬 또는 VPS에서 테스트
- **프로덕션 단계**: 클라우드 서버로 배포 (AWS, GCP 등)

**로컬 개발 환경:**
- Docker Compose로 FastAPI + PostgreSQL + Redis 통합 구성
- 로컬에서 전체 스택 테스트 가능

---

#### 옵션 2: Node.js + Express (TypeScript)
**장점:**
- JavaScript 생태계 통일 (모바일 앱과 동일 언어)
- 실시간 기능 구현 용이 (WebSocket)
- 높은 I/O 성능
- 풍부한 npm 패키지

**단점:**
- 복잡한 수학 계산 구현 시 Python보다 불리
- 지리 데이터 처리 라이브러리가 Python보다 제한적

**추천 라이브러리:**
- 웹 프레임워크: `Express` 또는 `NestJS`
- 지리 데이터: `turf.js`, `geolib`
- ORM: `TypeORM` 또는 `Prisma`

**비용:** 무료 (오픈소스)

---

### 결정 필요 사항
- [x] **선택:** Python + FastAPI
- [x] **이유:** 수학 라이브러리 사용이 필요할 수 있음
- [x] **구현 전략:** 로컬 Docker Compose 환경 → 프로토타입 테스트 → 프로덕션 배포

---

## 3. 데이터베이스

### 선택 사항

#### 옵션 1: PostgreSQL + PostGIS ⭐ 권장
**장점:**
- 지리 데이터 처리 최적화
- 공간 쿼리 지원 (ST_Distance, ST_Within 등)
- 강력한 인덱싱 (GIST 인덱스)
- ACID 트랜잭션 보장
- 오픈소스

**단점:**
- 설정 및 관리 복잡도가 MongoDB보다 높음
- 스키마 변경 시 마이그레이션 필요

**사용 사례:**
- 코스 데이터 저장 (폴리라인)
- 사용자 위치 기반 검색
- 공간 쿼리 (반경 내 코스 검색)

**비용:** 무료 (오픈소스)

**구현 전략:**
- **개발 단계**: Docker로 로컬 PostgreSQL + PostGIS 실행
- **프로토타입**: 로컬 또는 VPS에서 테스트
- **프로덕션 단계**: 클라우드 관리형 서비스 (AWS RDS, GCP Cloud SQL) 또는 자체 서버

**로컬 개발 환경:**
- Docker Compose로 PostgreSQL + PostGIS 컨테이너 실행
- 로컬에서 공간 쿼리 테스트 및 개발

---

#### 옵션 2: MongoDB
**장점:**
- 유연한 스키마
- JSON 형태의 지리 데이터 저장 용이
- 수평 확장 용이
- 빠른 개발 속도

**단점:**
- 공간 쿼리 기능이 PostGIS보다 제한적
- 지리 데이터 인덱싱이 PostgreSQL보다 약함
- 트랜잭션 지원 제한적

**사용 사례:**
- 코스 메타데이터 저장
- 사용자 데이터 저장

**비용:** 무료 (Community Edition)

---

### 결정 필요 사항
- [x] **선택:** PostgreSQL + PostGIS
- [x] **이유:** 지리 검색에 유리한 DB 사용
- [x] **구현 전략:** 로컬 Docker 환경 → 프로토타입 테스트 → 프로덕션 배포

**참고:** 지리 데이터 처리가 핵심이므로 PostgreSQL + PostGIS 강력 권장

---

## 4. 지도 API

### 선택 사항

#### 옵션 1: Google Maps SDK
**장점:**
- 가장 정확하고 상세한 지도
- 전 세계 커버리지 우수
- 강력한 API 기능
- 안정적인 서비스

**단점:**
- **높은 비용** (월 사용량 기반)
  - Maps SDK: 월 200달러 무료 크레딧 이후 $7/1000회
  - Directions API: $5/1000회
- 라이선스 제한 (특정 용도 제한)
- 커스터마이징 제한적

**예상 비용 (월 10,000 사용자 기준):**
- 지도 로드: 약 $50-100/월
- 총 예상: $100-200/월

---

#### 옵션 2: Mapbox SDK ⭐ 권장
**장점:**
- 커스터마이징 가능 (스타일, 레이어)
- 합리적인 가격
- 오픈소스 기반
- 좋은 성능
- 개발자 친화적

**단점:**
- Google Maps보다 일부 지역 데이터 부족 가능
- 초기 설정 필요

**예상 비용 (월 10,000 사용자 기준):**
- 지도 로드: 약 $30-50/월
- 총 예상: $50-100/월

**추천 라이브러리:**
- React Native: `@rnmapbox/maps`
- Flutter: `mapbox_maps_flutter`

---

#### 옵션 3: OpenStreetMap (OSM) + react-native-maps + TileServer GL ⭐ **최종 선택**
**장점:**
- **완전 무료** (오픈소스)
- 커뮤니티 기반
- 완전한 커스터마이징 가능
- 오프라인 사용 가능
- React Native에서 가장 안정적인 지도 라이브러리 사용
- OSM 데이터 직접 제어 및 가공 가능
- OSRM과 함께 사용 시 일관성 (둘 다 OSM 기반)
- 네이티브 성능 (react-native-maps는 네이티브 맵뷰 사용)

**단점:**
- 자체 서버 구축 필요 (TileServer GL)
- 초기 설정 복잡도 높음
- 지속적인 유지보수 필요
- 일부 지역 데이터 부족 가능 (OSM 데이터 품질에 따라)

**구성:**
- **라이브러리**: `react-native-maps`
- **타일 서버**: TileServer GL (Docker로 구축)
- **데이터**: OSM 데이터 (PBF → MBTiles 변환)

**구현 전략:**
- **개발 단계**: MapTiler 무료 티어로 빠른 시작 (OSM 스타일)
- **프로덕션 단계**: TileServer GL 자체 서버 구축 및 운영

**예상 비용:**
- 개발 단계: 무료 (MapTiler 무료 티어)
- 프로덕션: 서버 인프라 비용만 (약 $20-50/월)

**추천 라이브러리:**
- React Native: `react-native-maps`
- 타일 서버: TileServer GL (Docker)
- 데이터 변환: OpenMapTiles 도구

---

### 결정 필요 사항
- [x] **선택:** OSM + react-native-maps + TileServer GL
- [x] **이유:** 제약이 있는 사용 API 보다는 다양한 데이터를 확인하고 가공하고 싶음. OSRM과 함께 OSM 기반으로 통합 운영 가능
- [x] **예산 고려:** 개발 단계 무료, 프로덕션 $20-50/월 (서버 인프라)

---

## 5. 라우팅 API

### 선택 사항

#### 옵션 1: OSRM (Open Source Routing Machine) ⭐ 권장
**장점:**
- **완전 무료** (오픈소스)
- 보행/러닝 모드 지원
- 자체 서버 구축 가능
- API 호출 제한 없음
- 커스터마이징 가능

**단점:**
- 자체 서버 구축 및 관리 필요
- 초기 설정 복잡도 높음
- 서버 인프라 비용 발생
- OSM 데이터 기반 (지역별 품질 차이)

**구현 방법:**
- Docker 컨테이너로 OSRM 서버 구축
- OSM 데이터 다운로드 및 처리
- 자체 서버에서 호스팅

**예상 비용:**
- 서버 인프라: 약 $30-50/월 (AWS EC2)

---

#### 옵션 2: Google Directions API
**장점:**
- 정확한 라우팅
- 전 세계 커버리지 우수
- 안정적인 서비스
- 보행 모드 지원

**단점:**
- **높은 비용**
  - $5/1000회
  - 코스 생성 시 다수 호출로 비용 폭증
- API 호출 제한 (일일 할당량)

**예상 비용 (월 10,000 코스 생성, 코스당 평균 15회 호출):**
- 월 150,000회 호출 = $750/월
- **매우 높은 비용**

---

#### 옵션 3: Mapbox Directions API
**장점:**
- 합리적인 가격
- 보행 모드 지원
- 좋은 성능
- 지도 API와 통합 용이

**단점:**
- 비용 발생
- API 호출 제한

**예상 비용:**
- $0.50/1000회
- 월 150,000회 호출 = $75/월

---

#### 옵션 4: 하이브리드 접근 (권장)
**전략:**
- **주요 사용:** OSRM (자체 서버)
- **Fallback:** Mapbox Directions API (OSRM 실패 시)
- **캐싱:** Redis를 통한 적극적인 캐싱

**장점:**
- 비용 절감 (대부분 OSRM 사용)
- 안정성 확보 (Fallback 제공)
- 유연성

**예상 비용:**
- OSRM 서버: $30-50/월
- Mapbox Fallback: $10-20/월
- 총: $40-70/월

---

### 결정 필요 사항
- [x] **선택:** OSRM
- [x] **이유:** 로컬로 시험하다가 제품의 완성도가 높으면 서버를 운영 예정
- [x] **구현 전략:** 
  - 개발 단계: Docker로 로컬 OSRM 서버 실행
  - 프로토타입: 로컬 또는 VPS에서 테스트
  - 프로덕션: 자체 서버 구축 및 운영
- [x] **예산 고려:** 사용자 발생 시 재고려 예정

**참고:** 코스 생성 시 다수의 라우팅 API 호출이 필요하므로 OSRM 또는 하이브리드 접근 강력 권장

---

## 6. 캐싱 시스템

### 선택 사항

#### 옵션 1: Redis ⭐ 권장
**장점:**
- 빠른 성능 (인메모리)
- 다양한 데이터 구조 지원
- TTL (Time To Live) 지원
- 분산 캐싱 가능
- 세션 관리 용이

**사용 사례:**
- 코스 생성 결과 캐싱
- 라우팅 결과 캐싱
- 사용자 세션 관리

**비용:** 무료 (오픈소스) 또는 관리형 서비스 (AWS ElastiCache 등)

**구현 전략:**
- **개발 단계**: Docker로 로컬 Redis 실행
- **프로토타입**: 로컬 또는 VPS에서 테스트
- **프로덕션 단계**: 클라우드 관리형 서비스 (AWS ElastiCache, GCP Memorystore) 또는 자체 서버

**로컬 개발 환경:**
- Docker Compose로 Redis 컨테이너 실행
- 로컬에서 캐싱 로직 테스트 및 개발

---

#### 옵션 2: Memcached
**장점:**
- 단순하고 빠름
- 가벼움

**단점:**
- 데이터 구조 제한적
- TTL 기능 제한적

**비용:** 무료 (오픈소스)

---

### 결정 필요 사항
- [x] **선택:** Redis
- [x] **이유:** 많은 기능 제공
- [x] **구현 전략:** 로컬 Docker 환경 → 프로토타입 테스트 → 프로덕션 배포

**참고:** Redis가 더 많은 기능을 제공하므로 Redis 권장

---

## 7. 통신 프로토콜

### 선택 사항

#### 옵션 1: RESTful API ⭐ 권장
**장점:**
- 표준적이고 널리 사용됨
- 구현 단순
- 캐싱 용이
- 문서화 용이

**단점:**
- 실시간 업데이트에 제한적
- 오버페칭 가능

---

#### 옵션 2: GraphQL
**장점:**
- 필요한 데이터만 요청
- 타입 안정성
- 단일 엔드포인트

**단점:**
- 학습 곡선
- 복잡도 증가
- 캐싱 복잡

---

#### 옵션 3: RESTful + WebSocket (하이브리드)
**전략:**
- 일반 API: RESTful
- 실시간 업데이트 (코스 생성 진행률): WebSocket

**장점:**
- 각 프로토콜의 장점 활용
- 실시간 기능 지원

---

### 결정 필요 사항
- [x] **선택:** RESTful API
- [x] **이유:** 대중성

---

## 8. 인프라 및 배포

### 선택 사항

#### 옵션 1: AWS
**서비스:**
- EC2 (서버)
- RDS (PostgreSQL)
- ElastiCache (Redis)
- S3 (파일 저장)
- CloudFront (CDN)

**장점:**
- 전 세계 인프라
- 다양한 서비스
- 안정성

**예상 비용:** $100-200/월 (초기)

---

#### 옵션 2: Google Cloud Platform (GCP)
**서비스:**
- Compute Engine
- Cloud SQL (PostgreSQL)
- Memorystore (Redis)
- Cloud Storage

**장점:**
- 좋은 가격
- Kubernetes 통합

**예상 비용:** $80-150/월 (초기)

---

#### 옵션 3: Docker + 자체 서버
**장점:**
- 완전한 제어
- 비용 절감

**단점:**
- 관리 복잡도
- 확장성 제한

**예상 비용:** $30-50/월 (VPS)

---

### 결정 필요 사항
- [x] **선택:** 추후 재고려
- [x] **이유:** 
- [x] **예산 고려:** 
- [x] **구현 전략:**
  - **개발 단계**: Docker Compose로 로컬 환경 구성
    - FastAPI 서버 (로컬)
    - PostgreSQL + PostGIS (Docker)
    - Redis (Docker)
    - OSRM (Docker)
    - TileServer GL (Docker, 선택사항)
  - **프로토타입**: VPS 고려 ($30-50/월)
  - **프로덕션**: 사용자 증가 시 클라우드 전환 검토 (AWS/GCP)

---

## 9. 선택사항 기능

### 9.1 오프라인 지도 캐싱
- [x] **구현 여부:** 아니오
- [x] **이유:**

### 9.2 다크 모드
- [x] **구현 여부:** 예
- [x] **이유:**

### 9.3 가속도계/기압계 센서 활용
- [x] **구현 여부:** 예
- [x] **이유:**

### 9.4 WebSocket 실시간 업데이트
- [x] **구현 여부:** 아니오
- [x] **이유:**

---

## 10. 권장 조합 (비용 최적화)

### 옵션 A: 비용 최소화 (최종 선택)
- 모바일: React Native (TypeScript)
- 백엔드: Python + FastAPI
- 데이터베이스: PostgreSQL + PostGIS
- 지도: OSM + react-native-maps + TileServer GL
- 라우팅: OSRM (자체 서버)
- 캐싱: Redis
- 인프라: Docker + VPS (추후 재고려)

**예상 월 비용:** 
- 개발 단계: 무료 (로컬 환경)
- 프로토타입: $30-50/월 (VPS)
- 프로덕션: $50-80/월 (서버 인프라)

---

### 옵션 B: 균형 (권장)
- 모바일: React Native
- 백엔드: Python + FastAPI
- 데이터베이스: PostgreSQL + PostGIS
- 지도: Mapbox SDK
- 라우팅: OSRM (주) + Mapbox Directions (Fallback)
- 캐싱: Redis
- 인프라: AWS 또는 GCP

**예상 월 비용:** $100-150

---

### 옵션 C: 최고 품질
- 모바일: React Native 또는 네이티브
- 백엔드: Python + FastAPI
- 데이터베이스: PostgreSQL + PostGIS
- 지도: Google Maps SDK
- 라우팅: Google Directions API
- 캐싱: Redis
- 인프라: AWS

**예상 월 비용:** $300-500

---

## 11. 최종 결정 체크리스트

각 항목에 대해 선택하고 이유를 기록하세요:

1. [x] 모바일 앱 프레임워크: **React Native (TypeScript)**
   - 이유: 지도 라이브러리 사용 가능, 크로스 플랫폼 개발 효율성

2. [x] 백엔드 프레임워크: **Python + FastAPI**
   - 이유: 수학 라이브러리 사용 필요, 지리 데이터 처리 라이브러리 풍부

3. [x] 데이터베이스: **PostgreSQL + PostGIS**
   - 이유: 지리 검색에 유리한 DB 사용, 공간 쿼리 지원

4. [x] 지도 API: **OSM + react-native-maps + TileServer GL**
   - 이유: 제약 없는 API로 데이터 확인 및 가공 가능, OSRM과 통합 운영
   - 구성: react-native-maps + TileServer GL (자체 서버)

5. [x] 라우팅 API: **OSRM**
   - 이유: 로컬로 시험하다가 제품 완성도가 높으면 서버 운영 예정
   - 예산: 사용자 발생 시 재고려 예정

6. [x] 캐싱 시스템: **Redis**
   - 이유: 많은 기능 제공, TTL 지원, 분산 캐싱 가능

7. [x] 통신 프로토콜: **RESTful API**
   - 이유: 대중성, 구현 단순, 캐싱 용이

8. [x] 인프라: **추후 재고려**
   - **개발 단계**: Docker Compose로 로컬 환경 구성
     - FastAPI 서버 (로컬)
     - PostgreSQL + PostGIS (Docker)
     - Redis (Docker)
     - OSRM (Docker)
     - TileServer GL (Docker, 선택사항)
   - **프로토타입**: VPS 고려 ($30-50/월)
   - **프로덕션**: 사용자 증가 시 클라우드 전환 검토 (AWS/GCP)

9. [x] 선택사항 기능:
   - 오프라인 지도 캐싱: 아니오
   - 다크 모드: 예
   - 가속도계/기압계 센서 활용: 예
   - WebSocket 실시간 업데이트: 아니오

---

**검토 완료 후 SRS 문서에 최종 결정 사항을 반영하고 SDS 작성 진행**

