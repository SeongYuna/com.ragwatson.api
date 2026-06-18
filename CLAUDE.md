# 백엔드 지침

> 행동 원칙(구현 전 사고·단순성·정밀한 수정·목표 중심 실행)은 루트 [`CLAUDE.md`](../CLAUDE.md)를 따른다.

---

## 5. 하네스 엔지니어링 — Wiki + LLM PKS

카파시식 하네스는 **프롬프트만**이 아니라 **지식·경계·검증**을 환경에 고정하는 것이다. 이 저장소는 **Wiki + LLM PKS(Project Knowledge System)** 로 그 지식 계층을 구현한다.

| 계층 | 역할 | 예시 |
|------|------|------|
| **Wiki** | 사람이 읽고 갱신하는 규범·도메인 설명 | `docs/`, `vault/backend/`, `CLAUDE.md` |
| **LLM 규칙** | 에이전트에 항상 또는 조건부로 실리는 **짧은 고삐** | `vault/backend/app-rules.md`, `vault/backend/scaffold-rules.md` |
| **PKS (코드 계약)** | Wiki와 1:1로 맞춘 **실행 가능한 진실** | 포트·DTO·스키마·provider·테스트 |

**PKS 원칙**

1. Wiki에 없는 관례를 **추측으로 도입하지 않는다.** 새 패턴이 필요하면 `vault/backend/`에 먼저 적거나 추가를 제안한다.
2. 코드·문서·규칙이 어긋나면 **구현을 멈추고** 불일치를 표면화한다.
3. 완료 조건은 **검증 가능**해야 한다. (테스트·린트·타입·CI)
4. 경로·레이어·네이밍은 아래 **백엔드 아키텍처** 절을 따른다.

---

## 6. 백엔드 아키텍처 (SOLID · 헥사고날 · 클린 · DDD)

백엔드 Python/FastAPI 코드는 **반드시 SOLID**를 준수하고, **헥사고날 + 클린 + DDD**를 함께 적용한다.

### 기술 스택

- **언어:** Python 3.13
- **프레임워크:** FastAPI (비동기)
- **ORM:** SQLAlchemy 2.x (AsyncSession)
- **DB:** PostgreSQL
- **AI:** Google Gemini (outbound adapter)
- **마이그레이션:** Alembic
- **테스트:** pytest + pytest-asyncio

### 경로 표기 (문서·규칙·에이전트 응답)

| 영역 | 표기 규칙 | 예 |
|------|-----------|-----|
| **앱 바운디드 컨텍스트** | `backend/`·`apps/` **생략**, 모듈명부터 | `titanic_m_learning/app/use_cases/james_cmd_interactor.py` |
| **공유 core** | `backend.core`로 시작 | `backend.core.database`, `backend.core.matrix_API_key.app.keymaker_api` |

> 실제 Python import는 `core.database` 등 런타임 `sys.path`에 맞춘다. **문서·리뷰·에이전트 설명**에서는 위 표기를 쓴다.

### 레이어와 의존 방향

```text
adapter/inbound   →  app (ports · use_cases · dtos · mappers)
                        ↓ ports/output
adapter/outbound  →  ORM · PG · Gemini · outbound mappers

domain            ←  app만 참조 (entity · value object). adapter는 domain을 직접 노출하지 않는다.
dependencies/*_provider.py  ←  유일한 조립 지점 (DIP)
```

| 레이어 | DDD · 클린 · 헥사고날 대응 | 책임 |
|--------|---------------------------|------|
| `adapter/inbound/api/v1` | Primary adapter | Router, HTTP 예외 |
| `adapter/inbound/api/schemas` | Primary adapter | Pydantic 요청·응답 스키마 |
| `adapter/inbound/api/mappers` | Primary adapter | 스키마 ↔ DTO 변환 (inbound) |
| `adapter/inbound/grpc` | Primary adapter | gRPC 엔드포인트 (확장 예정) |
| `adapter/inbound/websocket` | Primary adapter | WebSocket 엔드포인트 (확장 예정) |
| `app/ports/input` | Use case port | Input port (ABC) |
| `app/use_cases` | Application service | Interactor — 비즈니스 흐름, DTO만 사용 |
| `app/dtos` | Application model | Command / Query / Result (앱 경계 데이터) |
| `app/ports/output` | Repository port | Output port (ABC) |
| `adapter/outbound/pg` | Secondary adapter | Repository 구현, AsyncSession 주입 |
| `adapter/outbound/orm` | Persistence model | 테이블·FK·relationship (DB 전용) |
| `adapter/outbound/mappers` | Anti-corruption | DTO ↔ ORM 변환 (앱이 SQLAlchemy를 모름) |
| `adapter/outbound/gemini` | Secondary adapter | Gemini AI 연동 (SmithGeminiChatRepository) |
| `domain/entities` · `domain/value_objects` | Domain | 엔티티·VO |
| `dependencies/*_provider.py` | Composition root | Repository 팩토리 + UseCase 팩토리 (DIP 조립) |

### Provider 패턴 (DIP 조립 표준)

모든 `dependencies/*_provider.py`는 아래 패턴을 따른다.

```python
def get_X_repository(
        db: AsyncSession = Depends(get_db)
) -> XRepository:
    return XQueryPgRepository(session=db)

def get_X_use_case(
    repository: XRepository = Depends(get_X_repository)
) -> XUseCase:
    return XQueryInteractor(repository=repository)
```

- Repository 팩토리와 UseCase 팩토리를 **반드시 분리**한다.
- 생성자 파라미터는 `session=db` (키워드 인수)를 쓴다.
- 리턴 타입은 **포트(ABC)** 로 선언한다. 구현체 타입 사용 금지.
- 외부 서비스(Gemini 등) 리포지토리는 `db` 없이 별도 팩토리로 분리한다.

### SOLID — 백엔드 적용 기준

| 원칙 | 이 프로젝트에서의 검문 |
|------|------------------------|
| **S** Single Responsibility | Router는 HTTP만, Interactor는 유스케이스만, ORM mapper는 변환만 |
| **O** Open/Closed | 새 유스케이스·어댑터는 **포트 추가 + provider 조립**으로 확장; 기존 interactor 수정 금지 |
| **L** Liskov Substitution | `XUseCase` 등 포트 타입에 구현체를 바꿔 끼워도 호출부 변경 없음 |
| **I** Interface Segregation | Use case port와 repository port 분리; fat interface 금지 |
| **D** Dependency Inversion | Router → port; Interactor → output port; **구현체는 `*_provider.py`에서만** |

### 읽기/쓰기 분리

- **Command (James):** INSERT/UPDATE/DELETE만. `james_cmd_router.py`, `james_cmd_interactor.py`
- **Query (나머지):** SELECT만. 공유 mapper 파일로 두 경로를 섞지 않는다.

### 금지 · 허용

- **금지:** Router가 `*PgRepository`·ORM을 직접 import
- **금지:** Interactor·Output port가 FastAPI `Depends`·SQLAlchemy·Pydantic schema에 의존
- **금지:** ORM을 API response로 직접 반환
- **금지:** Provider 이외의 위치에서 구현체 직접 생성
- **허용:** Inbound mapper에서 VO(`Gender` 등)로 API 형식 변환
- **허용:** Provider에서 `Depends(get_db)`로 세션 주입

### 현재 바운디드 컨텍스트

| 앱 | 경로 | 비고 |
|----|------|------|
| **Titanic ML** | `backend/apps/titanic_m_learning/` | 타이타닉 데이터 분석 + Smith AI 채팅 |

### 앱별 참고 구현

각 바운디드 컨텍스트의 상세 경로·참고 구현은 앱 디렉터리의 CLAUDE.md를 따른다.

| 앱 | 파일 |
|----|------|
| Titanic ML | [`apps/titanic_m_learning/_docs/CLAUDE.md`](apps/titanic_m_learning/_docs/CLAUDE.md) |

세부 DB 규칙(PK `id` 정수 등)은 `vault/backend/entity-rules.md`를 따른다.

---

## 문서 맵 (그래프 링크)

[[backend/README]]
[[vault/backend/CLAUDE]]
