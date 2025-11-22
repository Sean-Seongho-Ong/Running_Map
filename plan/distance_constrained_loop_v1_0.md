# Distance-Constrained Loop Generation Algorithm  
## **v1.0 – Unified S–P, Step-Based, Adaptive Loop Generator**  
### (거리 기반 러닝 루프 생성 알고리즘 v1.0 – 최종 통합 버전)

---

# 0. 개요 (Overview)

이 문서는 **러닝 코스 자동 생성용 거리 기반 루프 알고리즘**의 최종 통합 버전(v1.0)을 정의한다.

v1.0은 다음 세 가지 아이디어를 모두 포함한다.

1. **S–P 기반 2-leg 루프 (v0.1)**  
   - 시작점 S와 터닝 포인트 P 두 점을 중심으로 S→P→S 루프 생성

2. **고정 step 기반 원둘레 분할 루프 (v0.2)**  
   - 목표 거리 D에 해당하는 이상적인 원을 만들고,  
     원 둘레를 일정 거리(step, 기본 1km) 단위로 쪼개어 점들을 만든 뒤,  
     각 점을 도로에 스냅하여 루프 구성

3. **양방향 Adaptive Step 피드백 (v0.3 확장)**  
   - 한 번 생성한 루프의 실제 길이 L과 목표 D를 비교하여,  
     - 너무 길면 step을 줄이고(shrink)  
     - 너무 짧으면 step을 늘리는(grow)  
   - 피드백 루프를 통해 D에 더 근접한 루프를 찾아가는 방식

v1.0은 **S–P 기반 루프와 Step 기반 루프를 모두 활용**하며,  
상황에 따라 다음 우선순위로 루프를 생성하는 것을 기본 전략으로 한다.

1. Step 기반 + Adaptive (v0.2 + v0.3 확장) 시도  
2. 실패 시 S–P 기반(v0.1) 시도  
3. 그래도 만족도가 낮으면 Out & Back / 인기 루트 추천 등 Fallback

---

# 1. 입력 및 목표

## 1.1 입력 값

- 시작점 (사용자 현재 위치)  
  - `S = (lat, lon)`
- 목표 거리  
  - `D` (단위: km, 예: 5, 10, 15, 21 등)
- 초기 스텝 길이  
  - `step_init` (기본: 1.0 km)
- 옵션 파라미터 (기본값 있지만 변경 가능)
  - `tolerance_ratio` (허용 오차 비율, 기본: 0.1 → ±10%)
  - `step_min`, `step_max`
  - 최대 반복 횟수 `max_iter`

## 1.2 목표

- 실제 도로/보행로를 따라 이동하는 **폐곡선 루프(Loop Route)** 생성
- 루프 길이 `L`이 목표 거리 `D`에 최대한 가깝도록
  - 기본 조건:  
    \\(|L - D| \le tolerance\_ratio \cdot D\\)

- 루프는 다음 특성을 최대한 만족하는 것이 바람직하다.
  - 불필요한 자기 교차 최소화
  - 보행/러닝에 적합한 도로 위주
  - 과도한 고저차 피하거나, 옵션에 따라 선택적으로 반영

---

# 2. 기하학적 기본 개념

## 2.1 이상적인 원 기반 모델

목표 거리 D를 **이상적인 원형 러닝 루프**로 본다.

- 원의 둘레:
  \\[
  2\pi R \approx D
  \\]
- 이상적인 반지름:
  \\[
  R = \frac{D}{2\pi}
  \\]

이 원을 기준으로 두 가지 방식으로 루프를 만든다.

1. **S–P 기반**:  
   - S를 원 위의 한 점으로 보고, 지름 반대편 점을 P로 가정  
   - S–P 직선 거리:
     \\[
     |SP| = 2R = \frac{D}{\pi}
     \\]

2. **Step 기반**:  
   - 원 둘레를 일정 길이 `step`(예: 1km)로 등분하여 N개의 스텝 포인트 생성  
   - 각 포인트를 실제 도로로 스냅해서 루프 구성

---

# 3. 알고리즘 구성 요소

## 3.1 v0.1 – S–P 기반 2-leg 루프

### 3.1.1 개념

- S에서 시작해 멀리 떨어진 P까지 간 뒤,
- 다른 경로(또는 같은 경로)를 통해 S로 돌아오는 2-leg 루프

### 3.1.2 절차 요약

1. `R = D / (2π)` 계산
2. S에서 거리 `|SP| ≈ D/π`가 되도록 여러 방향(θ)으로 P 후보 생성
3. 각 후보 P에 대해:
   - S → P 최단 경로 (보행/러닝 모드)
   - P → S 최단 경로 (가능하면 다른 길 유도)
4. 루프 길이 L = d(S→P) + d(P→S)
5. `|L - D|` 및 기타 품질 지표 기반으로 상위 루프 선택

### 3.1.3 장점/단점

- 장점:
  - 구조 단순, 계산량 적음
- 단점:
  - 루프 형태가 단순(왕복 + 약간의 변형)
  - S–P 위치에 따라 루프가 편향되거나 지저분해질 수 있음

---

## 3.2 v0.2 – 고정 Step 기반 원둘레 분할 루프

### 3.2.1 개념

- 목표 거리 D에 해당하는 원을 만들고,
- 원 둘레를 **step(기본 1km)** 단위로 등분해서 N개 포인트(Qi) 생성
- 각 Qi를 주변 도로 노드 Vi로 스냅하고,
- Vi → V(i+1)을 라우팅하여 전체 루프 구성

### 3.2.2 절차

1. `R = D / (2π)` 계산
2. `step` 설정 (기본 1.0 km)
3. 예상 스텝 개수:
   \\[
   N \approx \frac{D}{step}
   \\]

4. 각 스텝에 대한 각도 증가량:
   \\[
   \Delta\theta = \frac{step}{R}
   \\]

5. 이상적인 포인트 Q 생성:
   - Q0 = S
   - Qi = S 기준 반지름 R, 각도 i·Δθ 오프셋으로 생성 (지리 좌표 변환)

6. 각 Qi를 도로상 포인트 Vi로 스냅:
   - 주변 반경 (100~300m) 내 보행 가능한 노드 검색
   - 적절한 노드 없으면 θ 미세 조정 또는 스킵

7. Vi → V(i+1) 라우팅 (보행/러닝 모드)
8. V(N-1) → S 라우팅으로 루프 닫기
9. 전체 거리 L 계산 및 품질 평가

### 3.2.3 특징

- 루프 형태가 더 "둥글고 자연스러운" 형태가 되기 쉽다
- step이 클수록 계산량↓, 정밀도↓  
  step이 작을수록 계산량↑, 정밀도↑

---

## 3.3 v0.3 – Adaptive Step Feedback (기본: 줄이기)

v0.3에서는 **고정 step으로 v0.2를 실행한 뒤,**  
실제 루프 길이 L과 목표 D를 비교하여

- 편차가 크면 → step을 줄이고 다시 실행하는 **피드백 루프**를 추가했다.

하지만 v0.3 초기안은 "줄이는 방향(shrink)"만 존재했고,  
거리 L이 너무 짧은 경우에 대한 "늘리는 방향(grow)" 전략은 포함되지 않았다.

---

# 4. v1.0 – 양방향 Adaptive Step + S–P Fallback

v1.0은 다음과 같은 **최종 통합 구조**를 가진다.

1. **Step 기반 + 양방향 Adaptive Step** (메인 알고리즘)
2. 실패 또는 품질 불만족 시 **S–P 기반 루프 시도**
3. 둘 다 만족스럽지 않으면 **Fallback (Out & Back / 인기 루트)**

## 4.1 Adaptive Step 논리 (양방향)

### 4.1.1 상태 판단

- 루프 길이 L과 목표 D 비교:
  - `error = |L - D|`
  - `rel_error = error / D`

### 4.1.2 기준

- 허용 오차 비율: `tolerance_ratio` (예: 0.1 → 10%)

- 세 구간으로 나눔:
  1. `rel_error <= tolerance_ratio`  
     → **OK: 수용 가능한 루프**
  2. `L > D` AND `rel_error > tolerance_ratio`  
     → **루프가 너무 김 → step 줄이기 (shrink)**
  3. `L < D` AND `rel_error > tolerance_ratio`  
     → **루프가 너무 짧음 → step 늘리기 (grow)**

### 4.1.3 step 조정 규칙

- shrink (너무 길 때):
  \\[
  step_{new} = \max(step \cdot shrink\_factor,\ step_{min})
  \\]
  - 예: `shrink_factor = 0.8`

- grow (너무 짧을 때):
  \\[
  step_{new} = \min(step \cdot grow\_factor,\ step_{max})
  \\]
  - 예: `grow_factor = 1.2`

단, 너무 극단적 step 값으로 가지 않도록  
`step_min`, `step_max` 범위 내로 제한한다.

### 4.1.4 반복 종료 조건

- `rel_error <= tolerance_ratio`  
  → 목표 오차 범위 내 도달
- 반복 횟수 `>= max_iter`  
  → 더 이상 개선 시도 중단, best-effort 선택
- `step`이 더 이상 변하지 않을 경우  
  (`step_new == step`) → 수렴/교착으로 보고 종료

---

# 5. v1.0 메인 루프 플로우

## 5.1 파라미터

- `step_init` : 1.0 km (예시)
- `step_min` : 0.4 km
- `step_max` : 2.0 km
- `tolerance_ratio` : 0.1 (±10%)
- `shrink_factor` : 0.8
- `grow_factor` : 1.2
- `max_iter` : 5~7
- `use_SP_fallback` : True/False 옵션

## 5.2 의사코드 – Step 기반 + Adaptive

```python
def generate_loop_v10_main(S, D,
                           step_init=1.0,
                           step_min=0.4,
                           step_max=2.0,
                           tolerance_ratio=0.1,
                           shrink_factor=0.8,
                           grow_factor=1.2,
                           max_iter=5,
                           use_SP_fallback=True):

    step = step_init
    best_loop = None
    best_L = None
    best_error = float("inf")
    best_rel_error = float("inf")

    for i in range(max_iter):
        loop, L, score = generate_loop_v02(S, D, step)  # v0.2 호출

        error = abs(L - D)
        rel_error = error / D

        # best loop 갱신
        if rel_error < best_rel_error:
            best_rel_error = rel_error
            best_error = error
            best_L = L
            best_loop = (loop, L, score, step, i+1)

        # 허용 오차 범위 안이면 성공
        if rel_error <= tolerance_ratio:
            return {
                "status": "OK",
                "loop": loop,
                "length": L,
                "score": score,
                "step_used": step,
                "iterations": i+1,
                "rel_error": rel_error,
                "algorithm": "STEP_ADAPTIVE"
            }

        # step 조정
        if L > D and rel_error > tolerance_ratio:
            # 루프가 너무 김 → step 줄이기
            new_step = max(step * shrink_factor, step_min)
        elif L < D and rel_error > tolerance_ratio:
            # 루프가 너무 짧음 → step 늘리기
            new_step = min(step * grow_factor, step_max)
        else:
            new_step = step

        # 더 이상 변할 수 없으면 종료
        if new_step == step:
            break

        step = new_step

    # Adaptive Step 기반으로는 허용 오차 내에 못 들어간 경우
    # best-effort 기반 결과를 반환하거나, S-P Fallback을 시도
    if use_SP_fallback:
        sp_result = generate_loop_SP_fallback(S, D)
        # Fallback 결과와 best_step 결과를 비교해서 더 나은 것 선택
        chosen = choose_better_result(best_loop, sp_result, D, tolerance_ratio)
        return chosen

    # Fallback 사용 안하면 best-effort 반환
    loop, L, score, step_used, iters = best_loop
    return {
        "status": "BEST_EFFORT",
        "loop": loop,
        "length": L,
        "score": score,
        "step_used": step_used,
        "iterations": iters,
        "rel_error": best_rel_error,
        "algorithm": "STEP_ADAPTIVE"
    }
```

## 5.3 S–P Fallback (v0.1 활용)

```python
def generate_loop_SP_fallback(S, D):
    # 여러 방향으로 P 후보 생성 후,
    # S→P, P→S 경로를 구해 루프 생성
    # v0.1 알고리즘을 캡슐화한 함수
    # 결과 형식은 v10_main과 동일한 dict로 맞춘다고 가정

    # ...
    return {
        "status": "OK" or "BEST_EFFORT" or "FAIL",
        "loop": loop_or_None,
        "length": L_or_None,
        "score": score_or_None,
        "step_used": None,
        "iterations": num_candidates_tried,
        "rel_error": rel_error_or_None,
        "algorithm": "SP_BASED"
    }
```

## 5.4 결과 선택 로직 예시

```python
def choose_better_result(step_result, sp_result, D, tolerance_ratio):
    # 둘 중 status가 OK인 쪽을 우선
    # 둘 다 OK면, rel_error가 작은 쪽
    # 둘 다 BEST_EFFORT면, 마찬가지로 rel_error 작은 쪽
    # 한쪽이 FAIL이면 다른 쪽 선택

    candidates = []
    for r in [step_result, sp_result]:
        if r is None:
            continue
        if r["status"] in ["OK", "BEST_EFFORT"]:
            candidates.append(r)

    if not candidates:
        return {
            "status": "FAIL",
            "loop": None,
            "length": None,
            "score": None,
            "step_used": None,
            "iterations": 0,
            "rel_error": None,
            "algorithm": None
        }

    # rel_error 기준 최선 선택
    best = min(candidates, key=lambda r: r.get("rel_error", 1e9))
    return best
```

---

# 6. Fallback 전략 요약

1. **Adaptive Step 기반 Step-Loop 실패 또는 품질 부족**
   - S–P 기반(v0.1) 루프 생성 시도

2. **S–P 기반도 만족스럽지 않을 때**
   - Out & Back:
     - S에서 D/2 근처까지 직선형 경로 라우팅 후 왕복
   - 인기 루트 추천:
     - 해당 지역에서 자주 사용되는 코스 중 거리 근사값 추천

3. 결과 상태 플래그
   - `"OK"`: tolerance 이내
   - `"BEST_EFFORT"`: 시도는 성공했지만 tolerance 초과
   - `"FAIL"`: 루프 생성을 포기

---

# 7. 검토 및 개선 포인트

v1.0은 **실제로 구현 가능한 수준**의 통합 알고리즘 설계이며,  
다음 항목들을 실험/튜닝 통해 개선할 수 있다.

1. **tolerance_ratio**  
   - ±10%가 적절한지, 러너 경험 기준 ±5%로 줄이는 게 맞는지
2. **shrink_factor / grow_factor**  
   - 0.8 / 1.2 조합이 수렴에 도움이 되는지  
   - 특정 환경에서는 더 aggressive하게 0.7 / 1.3이 나은지
3. **step_min / step_max**  
   - 도시 vs 산책로 vs 교외에 따라 다르게 둘 필요가 있는지
4. **S–P Fallback 비중**  
   - Step 기반이 잘 안 먹히는 지역(도로망 단순/불규칙)에서  
     S–P가 더 좋은 결과를 주는지 실측 필요
5. **Self-intersection 필터링 강도**  
   - 루프 중복/교차를 어느 정도까지 허용할지
6. **고저차 / 도로 종류 기반 추가 스코어링**  
   - 향후에는 `rel_error` 뿐 아니라,  
     사용자 취향(평지 선호, 언덕 러닝 선호, 강변 선호 등)에 따라  
     코스 선호도를 재정렬하는 고급 스코어링 레이어 추가 가능

---

# 8. 요약 (한 줄 정리)

> **v1.0 = 원 기반 거리 모델 + Step 분할 + 양방향 Adaptive Step + S–P Fallback까지 모두 포함한,  
> 실제 러닝 코스 자동 생성에 사용할 수 있는 통합 거리 기반 루프 생성기이다.**

