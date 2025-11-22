# UI Integration Plan

## 목표
프론트엔드 UI 화면을 백엔드 API와 연결하여 전체 데이터 흐름을 완성합니다.

## 전제 조건
- 백엔드는 임시 더미 코스를 반환하도록 설정 (알고리즘은 나중에 구현)
- 프론트엔드 API 클라이언트 및 Repository는 이미 구현됨

## 작업 순서

### 1. 백엔드: 임시 코스 생성 로직 추가
**파일:** `backend/application/use_cases/generate_course.py`

**목적:** 실제 알고리즘 없이 임시로 사각형 코스를 반환

**구현:**
- 시작점 주변 1km 사각형 코스 생성
- 4개의 좌표로 구성된 간단한 루프
- 실제 알고리즘은 나중에 교체

---

### 2. 프론트엔드: CourseGenerationScreen 연동
**파일:** `mobile/src/interface/screens/CourseGenerationScreen.tsx`

**작업:**
- [x] 거리 입력 필드 추가
- [x] "코스 생성" 버튼 클릭 시 `useCourseStore().generateCourse()` 호출
- [x] 로딩 상태 표시 (`isGenerating`)
- [x] 성공 시 코스 상세 정보 표시 (CourseDetailInfo 컴포넌트)
- [x] 코스 재생성 기능
- [x] 실패 시 에러 알림 표시
- [x] UX 개선 (네비게이션 흐름 수정)

---

### 3. 프론트엔드: MapScreen 업데이트
**파일:** `mobile/src/interface/screens/MapScreen.tsx`

**작업:**
- [x] 생성된 코스(`generatedCourse`)를 지도에 표시
- [x] 네비게이션 연결 (CourseGenerationScreen, CoursesTab)
- [x] 지도 제어 기능 (줌, 팬, 현재 위치 버튼)
- [x] UX 개선 (네비게이션 흐름 수정)

---

### 4. 프론트엔드: Navigation 설정
**파일:** `mobile/src/interface/navigation/AppNavigator.tsx`

**작업:**
- [x] Stack Navigator 설정
- [x] MapScreen, CourseGenerationScreen, RunningScreen 연결
- [x] 화면 간 파라미터 전달 설정

---

### 5. 프론트엔드: RunningScreen 연동 (선택사항)
**파일:** `mobile/src/interface/screens/RunningScreen.tsx`

**작업:**
- [ ] GPS 위치 추적 시작
- [ ] `useRunningStore().startRunning()` 호출
- [ ] 주기적으로 `updateLocation()` 호출
- [ ] 종료 시 `finishRunning()` 호출

---

## 검증 계획

1. **백엔드 서버 실행**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. **모바일 앱 실행**
   ```bash
   cd mobile
   npm start
   # Android Emulator에서 실행
   ```

3. **테스트 시나리오**
   - [x] CourseGenerationScreen에서 거리 입력 (예: 5km)
   - [x] "코스 생성" 버튼 클릭
   - [x] 로딩 스피너 표시 확인
   - [x] 코스 상세 정보 표시 확인
   - [ ] ⚠️ 앱 로드 문제로 인해 실제 테스트 미완료
   - [ ] MapScreen으로 이동하여 생성된 코스 확인 (앱 로드 후 테스트 필요)
   - [ ] 지도에 폴리라인이 그려지는지 확인 (앱 로드 후 테스트 필요)

---

## 현재 상태 (2025-11-22)

### 완료된 작업 ✅
- ✅ CourseGenerationScreen 연동 완료
- ✅ MapScreen 연동 완료
- ✅ 코스 상세 정보 표시 (CourseDetailInfo)
- ✅ 코스 재생성 기능
- ✅ UX 개선 (네비게이션 흐름)
- ✅ TypeScript 오류 수정

### 현재 문제 ⚠️
- ⚠️ **앱 로드 실패**: Android Studio 빌드는 성공했지만 앱이 JavaScript 번들을 로드하지 못함
  - Metro Bundler 연결 문제
  - WebSocket 연결 오류
  - Expo Dev Client에서 서버 선택 후 로드되지 않음

## 다음 단계 (이후 작업)

1. **프론트엔드 앱 로드 문제 해결** (우선순위 높음)
   - Metro Bundler 연결 문제 해결
   - Expo Dev Client 방식으로 앱 정상 실행 확인
   - 실제 앱 테스트 진행

2. **코스 생성 알고리즘 구현**
   - `DistanceConstrainedLoopGenerator` 구현
   - OSRM 라우팅 연동
   - 실제 도로를 따라가는 루프 생성

3. **러닝 추적 기능 완성**
   - GPS 위치 추적
   - 실시간 통계 계산
   - 백엔드 동기화

4. **코스 목록 및 상세 화면**
   - CourseListScreen 구현
   - 저장된 코스 목록 표시
   - 코스 상세 정보 표시
