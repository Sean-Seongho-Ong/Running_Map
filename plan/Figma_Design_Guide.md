# Figma 디자인 작업 가이드
## Running Map App - 프로세스 B 실행 가이드

**작성일:** 2024  
**목적:** 디자이너 없이 Figma에서 UI/UX 설계를 진행하기 위한 상세 가이드

---

## 1. Figma 프로젝트 설정

### 1.1 새 프로젝트 생성

1. Figma에서 새 파일 생성
2. 파일명: "Running Map App - UI/UX Design"
3. 프레임 설정:
   - iPhone 14 Pro (390 x 844) - iOS 기본
   - Pixel 6 (412 x 915) - Android 기본

### 1.2 템플릿 활용

**무료 템플릿 다운로드:**
- Material Design Kit for Figma
- iOS Design Kit for Figma
- React Native UI Kit

**사용 방법:**
1. Figma Community에서 템플릿 검색
2. 템플릿 복제
3. 필요한 컴포넌트만 복사하여 프로젝트에 사용

---

## 2. Phase 1: 사용자 플로우 다이어그램 (Day 1-2)

### 2.1 코스 생성 플로우

**플로우 단계:**
```
1. MapScreen (시작)
   ↓
2. 거리 입력 다이얼로그/화면
   ↓
3. 코스 생성 요청 (API 호출)
   ↓
4. 생성 중 표시 (로딩 상태)
   ↓
5. 코스 미리보기 (지도에 폴리라인 표시)
   ↓
6. 저장/사용 선택
   ├─ 저장 → CourseListScreen으로 이동
   └─ 사용 → RunningScreen으로 이동
```

**Figma에서 작성:**
1. Frame 생성: "User Flow - Course Generation"
2. 각 단계를 Rectangle로 표현
3. 화살표로 연결
4. 각 단계에 화면명과 주요 액션 명시

### 2.2 러닝 추적 플로우

**플로우 단계:**
```
1. MapScreen 또는 CourseListScreen
   ↓
2. 코스 선택
   ↓
3. 러닝 시작 확인
   ↓
4. RunningScreen (러닝 중)
   ├─ 일시정지 → 일시정지 화면
   ├─ 재개 → RunningScreen으로 복귀
   └─ 종료 → 종료 확인
       ↓
5. 러닝 결과 화면
   ├─ 저장
   └─ 공유
```

**Figma에서 작성:**
- 위와 동일한 방식으로 플로우 다이어그램 작성

### 2.3 화면 목록 정의

**핵심 화면:**
1. **MapScreen** - 지도 메인 화면
2. **CourseGenerationScreen** - 코스 생성 화면
3. **RunningScreen** - 러닝 추적 화면
4. **CourseListScreen** - 코스 목록 화면

**보조 화면:**
5. **CourseDetailScreen** - 코스 상세 정보
6. **RunningResultScreen** - 러닝 결과
7. **SettingsScreen** - 설정 화면

---

## 3. Phase 2: 핵심 화면 와이어프레임 (Day 3-5)

### 3.1 MapScreen 와이어프레임

**레이아웃 구조:**
```
┌─────────────────────────┐
│      지도 영역 (70%)      │
│                          │
│   [현재 위치 마커]        │
│   [코스 폴리라인]         │
│                          │
├─────────────────────────┤
│   하단 버튼 영역 (30%)    │
│  [코스 생성] [내 코스]    │
└─────────────────────────┘
```

**Figma 작업:**
1. Frame 생성: "MapScreen - Wireframe"
2. 지도 영역: Rectangle (배경색: #E8F5E9)
3. 현재 위치 마커: Circle (색상: #FF6B35)
4. 코스 폴리라인: Line (색상: #FF6B35, 두께: 4px)
5. 하단 버튼 영역: Rectangle (배경색: #FFFFFF)
6. 버튼: Rectangle with Text (색상: #FF6B35)

**요소:**
- 지도 영역: 전체 화면의 70%
- 하단 버튼 영역: 30%
- 현재 위치 마커: 지도 중앙
- 코스 폴리라인: 지도 위에 오버레이

### 3.2 CourseGenerationScreen 와이어프레임

**레이아웃 구조:**
```
┌─────────────────────────┐
│      지도 영역 (60%)      │
│   [현재 위치]            │
│   [생성된 코스 미리보기]  │
├─────────────────────────┤
│   입력 영역 (40%)        │
│   거리 입력: [____] km   │
│   [3km] [5km] [10km]    │
│   [생성하기] 버튼        │
│   [로딩 상태 표시]       │
└─────────────────────────┘
```

**Figma 작업:**
1. Frame 생성: "CourseGenerationScreen - Wireframe"
2. 지도 영역: Rectangle (60% 높이)
3. 입력 영역: Rectangle (40% 높이)
4. 거리 입력 필드: Rectangle with Text
5. 프리셋 버튼: 3개의 작은 Rectangle
6. 생성 버튼: 큰 Rectangle (색상: #FF6B35)

**요소:**
- 지도: 60% 높이
- 입력 영역: 40% 높이
- 프리셋 버튼: 3km, 5km, 10km
- 생성 버튼: Primary 색상

### 3.3 RunningScreen 와이어프레임

**레이아웃 구조:**
```
┌─────────────────────────┐
│   통계 영역 (상단, 30%)   │
│   거리: 2.5 km           │
│   시간: 15:30            │
│   페이스: 6:12 /km       │
├─────────────────────────┤
│      지도 영역 (50%)      │
│   [현재 경로]            │
│   [현재 위치]            │
├─────────────────────────┤
│   컨트롤 버튼 (20%)       │
│   [일시정지] [종료]      │
└─────────────────────────┘
```

**Figma 작업:**
1. Frame 생성: "RunningScreen - Wireframe"
2. 통계 영역: 상단 Rectangle (30% 높이)
3. 통계 항목: Text (큰 폰트)
4. 지도 영역: 중앙 Rectangle (50% 높이)
5. 컨트롤 버튼: 하단 Rectangle (20% 높이)
6. 버튼: 2개의 Rectangle (일시정지, 종료)

**요소:**
- 통계: 큰 폰트로 표시 (48px)
- 지도: 현재 경로와 위치 표시
- 컨트롤: 하단 중앙 배치

### 3.4 CourseListScreen 와이어프레임

**레이아웃 구조:**
```
┌─────────────────────────┐
│   검색 바                │
│   [검색...]              │
├─────────────────────────┤
│   코스 카드 1            │
│   ┌─────────────────┐  │
│   │ 코스명: 5km 루프 │  │
│   │ 거리: 5.2 km     │  │
│   │ 생성일: 2024.01 │  │
│   └─────────────────┘  │
├─────────────────────────┤
│   코스 카드 2            │
│   ┌─────────────────┐  │
│   │ ...              │  │
│   └─────────────────┘  │
└─────────────────────────┘
```

**Figma 작업:**
1. Frame 생성: "CourseListScreen - Wireframe"
2. 검색 바: 상단 Rectangle with Text
3. 코스 카드: Rectangle (둥근 모서리, 그림자)
4. 카드 내용: Text 요소들

**요소:**
- 검색 바: 상단 고정
- 코스 카드: 스크롤 가능한 리스트
- 카드: 그림자 효과, 둥근 모서리

---

## 4. Phase 3: 기본 디자인 시스템 (Day 6-7)

### 4.1 색상 팔레트 정의

**Figma에서 Color Styles 생성:**

1. **Primary Colors**
   - Primary: #FF6B35
   - Primary Dark: #E85A2B
   - Primary Light: #FF8C5A

2. **Secondary Colors**
   - Secondary: #4ECDC4
   - Secondary Dark: #3BA8A0
   - Secondary Light: #6ED4CC

3. **Background Colors**
   - Background: #FFFFFF
   - Background Secondary: #F5F5F5
   - Surface: #FFFFFF
   - Surface Elevated: #FAFAFA

4. **Text Colors**
   - Text: #212121
   - Text Secondary: #757575
   - Text Disabled: #BDBDBD
   - Text Inverse: #FFFFFF

5. **Status Colors**
   - Success: #4CAF50
   - Error: #F44336
   - Warning: #FF9800
   - Info: #2196F3

6. **Dark Mode Colors**
   - Background: #121212
   - Surface: #1E1E1E
   - Text: #FFFFFF
   - Text Secondary: #B0B0B0

**작업 방법:**
1. Figma에서 색상 선택
2. 우클릭 → "Add to style"
3. 스타일명 지정 (예: "Primary")
4. 재사용 가능한 Color Style로 저장

### 4.2 타이포그래피 시스템 정의

**Figma에서 Text Styles 생성:**

1. **Headings**
   - H1: 32px, Bold (700), Line Height: 40px
   - H2: 24px, Semi-Bold (600), Line Height: 32px
   - H3: 20px, Semi-Bold (600), Line Height: 28px

2. **Body**
   - Body: 16px, Regular (400), Line Height: 24px
   - Body Bold: 16px, Semi-Bold (600), Line Height: 24px

3. **Caption**
   - Caption: 14px, Regular (400), Line Height: 20px
   - Caption Bold: 14px, Semi-Bold (600), Line Height: 20px

4. **Small**
   - Small: 12px, Regular (400), Line Height: 16px

5. **Running Stats**
   - Stat Large: 48px, Bold (700), Line Height: 56px
   - Stat Medium: 32px, Semi-Bold (600), Line Height: 40px
   - Stat Small: 24px, Semi-Bold (600), Line Height: 32px

**작업 방법:**
1. Text 요소 생성
2. 폰트 크기, 굵기, 줄 간격 설정
3. 우클릭 → "Add to style"
4. 스타일명 지정 (예: "H1")
5. 재사용 가능한 Text Style로 저장

### 4.3 간격 시스템 정의

**8px 그리드 시스템:**
- xs: 4px
- sm: 8px
- md: 16px
- lg: 24px
- xl: 32px
- xxl: 48px

**Figma에서 활용:**
1. Auto Layout 사용 시 간격 설정
2. Padding/Margin에 위 값 적용
3. 일관성 유지

### 4.4 기본 버튼 스타일 정의

**Primary Button:**
- 배경색: Primary (#FF6B35)
- 텍스트: Text Inverse (#FFFFFF)
- 높이: 44px (최소 터치 영역)
- 패딩: 24px (좌우)
- 모서리: 8px
- 폰트: Body Bold

**Secondary Button:**
- 배경색: Secondary (#4ECDC4)
- 텍스트: Text Inverse (#FFFFFF)
- 나머지 동일

**Outline Button:**
- 배경색: 투명
- 테두리: Primary (#FF6B35), 1px
- 텍스트: Primary (#FF6B35)
- 나머지 동일

**Text Button:**
- 배경색: 투명
- 텍스트: Primary (#FF6B35)
- 높이: 44px
- 패딩: 16px

**작업 방법:**
1. Rectangle 생성 (버튼 모양)
2. Text 추가
3. Auto Layout 적용
4. Component로 변환
5. Variants 생성 (Primary, Secondary, Outline, Text)

### 4.5 입력 필드 스타일 정의

**Input Field:**
- 높이: 48px
- 패딩: 16px (좌우)
- 배경색: Surface (#FFFFFF)
- 테두리: Border (#E0E0E0), 1px
- 모서리: 8px
- 폰트: Body (16px)
- Placeholder: Text Disabled (#BDBDBD)

**Error State:**
- 테두리: Error (#F44336)
- 에러 메시지: Caption, Error 색상

**작업 방법:**
1. Rectangle 생성 (입력 필드)
2. Text 추가 (Placeholder)
3. Component로 변환
4. Variants 생성 (Default, Error, Disabled)

---

## 5. Phase 4: 하이파이 프로토타입 (Day 8)

### 5.1 와이어프레임에 스타일 적용

**작업 순서:**
1. 와이어프레임 선택
2. 색상 스타일 적용
3. 타이포그래피 스타일 적용
4. 간격 조정
5. 그림자, 그라데이션 등 시각 효과 추가

### 5.2 인터랙션 연결

**Figma Prototype 기능 사용:**

1. **화면 간 전환**
   - 버튼 클릭 → 다음 화면으로 이동
   - 전환 애니메이션: Slide, Fade 등

2. **상태 변화**
   - 버튼 Hover 상태
   - 입력 필드 Focus 상태
   - 로딩 상태

**작업 방법:**
1. 요소 선택
2. 우측 패널에서 "Prototype" 탭 선택
3. 연결선을 다음 화면으로 드래그
4. 전환 애니메이션 설정
5. 트리거 설정 (On Click, On Drag 등)

### 5.3 애니메이션 정의

**전환 애니메이션:**
- 화면 전환: Slide (Left/Right), Duration: 300ms
- 모달 표시: Fade, Duration: 200ms
- 버튼 클릭: Scale (0.95), Duration: 100ms

**작업 방법:**
1. Prototype 연결 설정
2. Animation 선택
3. Duration 설정
4. Easing 설정 (Ease In/Out)

---

## 6. Figma 작업 체크리스트

### Phase 1 체크리스트
- [ ] 코스 생성 플로우 다이어그램 작성
- [ ] 러닝 추적 플로우 다이어그램 작성
- [ ] 화면 목록 정의
- [ ] 네비게이션 구조 정의

### Phase 2 체크리스트
- [ ] MapScreen 와이어프레임
- [ ] CourseGenerationScreen 와이어프레임
- [ ] RunningScreen 와이어프레임
- [ ] CourseListScreen 와이어프레임

### Phase 3 체크리스트
- [ ] 색상 팔레트 (Color Styles)
- [ ] 타이포그래피 시스템 (Text Styles)
- [ ] 간격 시스템 정의
- [ ] 버튼 컴포넌트 (Variants)
- [ ] 입력 필드 컴포넌트 (Variants)

### Phase 4 체크리스트
- [ ] 와이어프레임에 스타일 적용
- [ ] 인터랙션 연결
- [ ] 애니메이션 정의
- [ ] 프로토타입 테스트

---

## 7. Figma 파일 구조 권장사항

```
Running Map App - UI/UX Design
├── 01. User Flows
│   ├── Course Generation Flow
│   └── Running Tracking Flow
├── 02. Wireframes
│   ├── MapScreen
│   ├── CourseGenerationScreen
│   ├── RunningScreen
│   └── CourseListScreen
├── 03. Design System
│   ├── Colors
│   ├── Typography
│   ├── Spacing
│   ├── Components
│   │   ├── Buttons
│   │   └── Inputs
│   └── Icons
└── 04. High-Fidelity Prototypes
    ├── MapScreen - Final
    ├── CourseGenerationScreen - Final
    ├── RunningScreen - Final
    └── CourseListScreen - Final
```

---

## 8. 참고 자료

### Material Design
- URL: https://material.io/design
- 컴포넌트 가이드라인
- 색상 시스템
- 타이포그래피

### Human Interface Guidelines
- URL: https://developer.apple.com/design/human-interface-guidelines/
- iOS 디자인 원칙
- 컴포넌트 가이드라인

### 벤치마킹 앱
- Strava
- Nike Run Club
- Runkeeper
- MapMyRun

---

**이 가이드를 따라 Figma에서 디자인 작업을 진행하세요.**

