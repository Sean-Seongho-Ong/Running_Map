# React Native에서 OSM 사용을 위한 최적 조합

## 개요
React Native에서 OpenStreetMap(OSM)을 사용하는 방법과 각 옵션의 장단점을 정리합니다.

---

## 옵션 비교

### 옵션 1: react-native-maps + OSM 타일 서버 ⭐ **가장 권장**

#### 구성
- **라이브러리**: `react-native-maps`
- **타일 서버**: 자체 OSM 타일 서버 또는 공개 타일 서버
- **타일 제공자**: MapTiler, OpenMapTiles, 또는 자체 구축

#### 장점
- ✅ React Native에서 가장 성숙하고 안정적인 지도 라이브러리
- ✅ 널리 사용되어 커뮤니티 지원 풍부
- ✅ 네이티브 성능 (네이티브 맵뷰 사용)
- ✅ 다양한 기능 지원 (마커, 폴리라인, 클러스터링 등)
- ✅ OSM 타일 서버 URL만 설정하면 바로 사용 가능
- ✅ 오프라인 타일 캐싱 지원 가능

#### 단점
- ⚠️ OSM 타일 서버 구축 필요 (또는 공개 서버 사용)
- ⚠️ 타일 서버 비용 발생 가능

#### 구현 방법
```typescript
import MapView, { PROVIDER_DEFAULT } from 'react-native-maps';

<MapView
  provider={PROVIDER_DEFAULT}
  customMapStyle={[]} // OSM 스타일 적용
  urlTemplate="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
  // 또는 자체 타일 서버
  // urlTemplate="https://your-tile-server.com/{z}/{x}/{y}.png"
/>
```

#### 타일 서버 옵션
1. **공개 OSM 타일 서버** (제한 있음)
   - `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
   - 사용 제한: 초당 2회 요청
   - 프로덕션에는 부적합

2. **MapTiler** (상용, OSM 기반)
   - 무료 티어: 월 100,000 타일
   - 유료: $49/월부터
   - OSM 데이터 기반

3. **자체 타일 서버 구축**
   - **TileServer GL**: Docker로 쉽게 구축
   - **Mapnik + mod_tile**: 전통적인 방법
   - **PostgreSQL + PostGIS + Mapnik**: 완전한 제어

#### 추천 조합
- **개발/테스트**: 공개 OSM 타일 서버 (제한 있음)
- **프로덕션**: 자체 TileServer GL 구축 또는 MapTiler

---

### 옵션 2: react-native-mapbox-gl (MapLibre 기반)

#### 구성
- **라이브러리**: `@rnmapbox/maps` (구 react-native-mapbox-gl)
- **렌더링 엔진**: MapLibre GL (오픈소스, Mapbox GL 포크)
- **데이터 소스**: OSM 데이터

#### 장점
- ✅ MapLibre는 완전 오픈소스 (Mapbox GL의 포크)
- ✅ OSM 데이터 직접 사용 가능
- ✅ 벡터 타일 지원 (더 빠른 렌더링)
- ✅ 고급 스타일링 (Mapbox Style JSON)
- ✅ 3D 지도, 애니메이션 등 고급 기능
- ✅ 오프라인 지도 지원

#### 단점
- ⚠️ 설정이 react-native-maps보다 복잡
- ⚠️ 라이브러리 크기가 더 큼
- ⚠️ 벡터 타일 서버 구축 필요 (선택사항)

#### 구현 방법
```typescript
import Mapbox from '@rnmapbox/maps';

// OSM 스타일 사용
<Mapbox.MapView
  styleURL="mapbox://styles/mapbox/streets-v11" // 또는 OSM 스타일
  style={{ flex: 1 }}
>
  {/* 지도 내용 */}
</Mapbox.MapView>
```

#### OSM 스타일 옵션
1. **MapTiler OSM 스타일** (무료)
   - `https://api.maptiler.com/maps/openstreetmap/style.json`
   - API 키 필요 (무료 티어 제공)

2. **자체 벡터 타일 서버 구축**
   - **Tileserver GL**: OSM 데이터를 벡터 타일로 변환
   - **OpenMapTiles**: OSM 기반 벡터 타일 생성

#### 추천 조합
- **간단한 구현**: MapTiler OSM 스타일 사용
- **완전한 제어**: Tileserver GL + OSM 데이터

---

### 옵션 3: react-native-webview + Leaflet

#### 구성
- **라이브러리**: `react-native-webview`
- **지도 라이브러리**: Leaflet.js (웹뷰 내)
- **타일 소스**: OSM 타일

#### 장점
- ✅ Leaflet은 OSM과 완벽 호환
- ✅ 웹 기술 활용 가능
- ✅ 다양한 플러그인

#### 단점
- ❌ 성능이 네이티브보다 낮음
- ❌ 웹뷰 오버헤드
- ❌ 네이티브 기능 제한
- ❌ 권장하지 않음 (성능 문제)

---

## 최종 권장 조합

### 시나리오별 추천

#### 시나리오 A: 빠른 개발 + 비용 최소화 (권장)
```
- 라이브러리: react-native-maps
- 타일 서버: MapTiler (무료 티어) 또는 자체 TileServer GL
- 장점: 빠른 개발, 안정적, 비용 최소화
- 단점: 타일 서버 관리 필요 (자체 구축 시)
```

#### 시나리오 B: 고급 기능 + 완전한 제어
```
- 라이브러리: @rnmapbox/maps (MapLibre)
- 타일 서버: Tileserver GL + OSM 데이터
- 장점: 벡터 타일, 고급 스타일링, 완전한 제어
- 단점: 설정 복잡도 높음, 초기 구축 시간 필요
```

#### 시나리오 C: 하이브리드 접근
```
- 기본 지도: react-native-maps + OSM 타일
- 특수 기능: @rnmapbox/maps (필요 시)
- 장점: 각 라이브러리의 장점 활용
- 단점: 두 라이브러리 관리 필요
```

---

## 구체적인 구현 전략

### 전략 1: react-native-maps + TileServer GL (최적)

#### 1단계: TileServer GL 구축
```bash
# Docker로 TileServer GL 실행
docker run -d \
  -p 8080:80 \
  -v $(pwd)/data:/data \
  maptiler/tileserver-gl \
  --mbtiles /data/osm.mbtiles
```

#### 2단계: OSM 데이터 준비
```bash
# OSM 데이터 다운로드 (예: 한국)
wget https://download.geofabrik.de/asia/south-korea-latest.osm.pbf

# MBTiles로 변환 (OpenMapTiles 도구 사용)
```

#### 3단계: React Native에서 사용
```typescript
import MapView from 'react-native-maps';

<MapView
  provider={PROVIDER_DEFAULT}
  urlTemplate="http://your-server:8080/data/v3/{z}/{x}/{y}.pbf"
  // 또는
  customMapStyle={[]}
  tileUrlTemplate="http://your-server:8080/raster/{z}/{x}/{y}.png"
/>
```

### 전략 2: react-native-maps + MapTiler (간단)

#### 1단계: MapTiler 계정 생성
- 무료 계정 생성
- API 키 발급

#### 2단계: React Native 설정
```typescript
import MapView from 'react-native-maps';

<MapView
  provider={PROVIDER_DEFAULT}
  urlTemplate="https://api.maptiler.com/maps/openstreetmap/{z}/{x}/{y}.png?key=YOUR_API_KEY"
/>
```

### 전략 3: @rnmapbox/maps + OSM 스타일 (고급)

#### 1단계: 라이브러리 설치
```bash
npm install @rnmapbox/maps
```

#### 2단계: OSM 스타일 사용
```typescript
import Mapbox from '@rnmapbox/maps';

<Mapbox.MapView
  styleURL="https://api.maptiler.com/maps/openstreetmap/style.json?key=YOUR_KEY"
  style={{ flex: 1 }}
>
  <Mapbox.Camera
    zoomLevel={15}
    centerCoordinate={[longitude, latitude]}
  />
</Mapbox.MapView>
```

---

## 비용 비교

| 옵션 | 초기 비용 | 월 운영 비용 | 관리 복잡도 |
|------|----------|-------------|------------|
| react-native-maps + 공개 OSM | 무료 | 무료 | 낮음 (제한 있음) |
| react-native-maps + MapTiler | 무료 | $0-49/월 | 낮음 |
| react-native-maps + TileServer GL | 무료 | $20-50/월 (서버) | 중간 |
| @rnmapbox/maps + MapTiler | 무료 | $0-49/월 | 낮음 |
| @rnmapbox/maps + Tileserver GL | 무료 | $20-50/월 (서버) | 높음 |

---

## 최종 추천

### 현재 프로젝트에 가장 적합한 조합

**1순위: react-native-maps + TileServer GL**
- 이유:
  - React Native에서 가장 안정적
  - OSM 데이터 완전한 제어
  - 오프라인 지원 가능
  - 비용 효율적 (자체 서버)
  - OSRM과 함께 사용 시 일관성 (둘 다 OSM 기반)

**2순위: react-native-maps + MapTiler**
- 이유:
  - 빠른 시작
  - 관리 부담 적음
  - 무료 티어로 시작 가능
  - 프로덕션 확장 용이

**3순위: @rnmapbox/maps + MapTiler OSM 스타일**
- 이유:
  - 고급 스타일링 필요 시
  - 벡터 타일의 성능 이점
  - 3D 지도 등 고급 기능 필요 시

---

## 구현 단계별 가이드

### Phase 1: 개발 환경 (로컬)
1. react-native-maps 설치
2. 공개 OSM 타일 서버 사용 (제한 있음)
3. 기본 기능 구현

### Phase 2: 프로토타입
1. MapTiler 무료 계정 생성
2. MapTiler OSM 스타일 적용
3. 테스트 및 검증

### Phase 3: 프로덕션
1. TileServer GL 구축 (Docker)
2. OSM 데이터 다운로드 및 변환
3. 자체 타일 서버 운영
4. 오프라인 타일 캐싱 구현

---

## 결론

**React Native + OSM의 최적 조합:**
```
react-native-maps + TileServer GL (자체 서버)
또는
react-native-maps + MapTiler (빠른 시작)
```

이 조합이 현재 프로젝트의 요구사항(OSM 데이터 확인 및 가공, 비용 최소화, 자체 서버 운영 가능)에 가장 적합합니다.

