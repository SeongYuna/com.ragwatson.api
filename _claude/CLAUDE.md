# 백엔드 — 아키텍처 결정 기록 (ADR)

> 코드 수준 규칙은 [`backend/CLAUDE.md`](../../backend/CLAUDE.md)를 따른다.  
> 이 문서는 **왜** 그 규칙이 생겼는지의 맥락과 의사결정 기록을 담는다.

# 백엔드 지침
---

## 기술 선택 근거

### FastAPI + AsyncSession

- 타이타닉 데이터 분석은 DB 집계 쿼리가 많다. 동기 ORM은 워커를 블로킹하므로 `AsyncSession`을 선택했다.
- FastAPI의 `Depends` 시스템이 헥사고날 아키텍처의 DIP 조립(provider 패턴)과 자연스럽게 맞는다.

### 헥사고날 + 클린 아키텍처

- 어댑터(PG, Gemini, gRPC)를 교체할 때 비즈니스 로직(`app/use_cases/`)을 건드리지 않기 위해 선택했다.
- `adapter/outbound/gemini/`가 추가되면서 외부 AI 서비스도 동일한 포트-어댑터 구조로 수용할 수 있음을 확인했다.

### Provider 패턴 (Repository 팩토리 분리)

- 초기에는 `get_X_use_case(db: AsyncSession = Depends(get_db))` 단일 함수로 조립했다.
- Repository 단독 테스트 및 다중 Repository 주입(Smith: PG + Gemini)을 고려해 Repository 팩토리와 UseCase 팩토리를 분리하는 패턴으로 통일했다.
- `session=db` 키워드 인수: 위치 인수 혼동 방지를 위해 강제한다.

---

## 바운디드 컨텍스트 맵

```text
titanic_m_learning
├── Query (읽기): Andrew, Caledon, Hartley, Isador, Jack,
│                Lowe, Molly, Rose, Ruth, Walter, Smith
└── Command (쓰기): James
```

- **James (CMD):** 승객 데이터 INSERT. Command/Query 분리 원칙에 따라 별도 라우터·인터랙터·리포지토리를 가진다.
- **Smith (AI 채팅):** PG 통계 조회(SmithStatsPgRepository) + Gemini 응답 생성(SmithGeminiChatRepository) 두 포트를 사용하는 유일한 유스케이스다.

---

## 레거시 · 기술 부채

- `adapter/inbound/grpc/`, `adapter/inbound/websocket/` 디렉터리는 생성되어 있으나 구현 없음. 삭제하지 말고 확장 예정 경로로 유지한다.
- 일부 인터랙터가 FastAPI schema를 직접 import하는 위반이 있다. 점진적으로 DTO로 교체한다.

---

## 데이터 척도 (Measurement Scale)

### Categorical

데이터가 카테고리로 묶일 때 사용한다.

**nominal** : 이름을 바탕으로 하는 척도
순서와는 상관없이 그냥 셀 수 있는 정도의 데이터
ex) 청팀, 홍팀, 백팀

**ordinal** : 순서를 바탕으로 하는 척도
자료들 사이에 순서(서열)가 있는 경우
ex) 청팀이 이길 가능성 1. 매우 낮음 2. 낮음 3. 보통 4. 높음 5. 매우높음

### Quantitative

숫자로 셀 수 있을 때 사용한다.

**interval** : 간격을 바탕으로 하는 척도
기준이 없이 일정한 측정 구간을 갖는 데이터
ex) 11:00~11:05, 온도, ph (10배 덥다·시다 표현 불가)

**ratio** : 비율을 바탕으로 하는 척도
임의의 원점을 기준으로 두고 정하는 데이터
ex) 나이, 돈, 몸무게 (10배 많다 표현 가능)

---

## 규칙 인덱스

에이전트는 코드 작성 전 해당 영역 규칙을 읽고 따른다.

| 문서 | 적용 대상 | 요약 |
|------|-----------|------|
| [`backend/_claude/ENTITY_RULES.md`](./ENTITY_RULES.md) | `backend/**/*.py` (모델·마이그레이션) | PK는 정수 `id` 통일, SQLModel/SQLAlchemy 패턴 |
| [`backend/apps/paper_lens/_docs/PAPER_ERD.md`](../apps/paper_lens/_docs/PAPER_ERD.md) | 논문 리서치 도메인 | `users`, `papers` 스키마·ERD |

### 에이전트 지시 (복사용)

Backend (엔티티·DB) 작업 시:
```text
@backend/_claude/ENTITY_RULES.md 를 따르세요.
모든 테이블의 기본 키는 정수형 id 하나로 통일하고, 업무 키는 별도 컬럼으로 두세요.
```

규칙 추가 방법: `backend/_claude/` 에 `*-rules.md` 작성 후 위 표에 한 줄 추가.

---

## 관련 노트

[[backend/_claude/app-rules]]
[[backend/_claude/ENTITY_RULES]]
[[backend/_claude/scaffold-rules]]
[[backend/_claude/auth-rules]]
[[backend/_claude/db-rules]]
