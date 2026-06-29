---
type: hub
title: Starcraft Hub — Graph DB · Vector DB 파이프라인 전략
links:
  - starcraft/adapter
  - starcraft/app/ports
---

# Starcraft Hub — DB 파이프라인 전략

> Starcraft는 스타 토폴로지의 **중앙 허브**다.  
> 모든 스포크(spoke)는 이 허브의 공개 포트(Port)를 통해서만 지식 그래프와 벡터 인덱스에 접근한다.

---

## 1. 왜 두 가지 DB인가

| 질문 유형 | 적합한 DB | 이유 |
|-----------|-----------|------|
| "A와 B의 관계는?" "경로 탐색" | **Graph DB (Neo4j)** | 엔티티 간 관계·경로를 네이티브로 표현 |
| "이 문장과 가장 유사한 지식은?" | **Vector DB (Qdrant)** | 임베딩 기반 의미 유사도 검색 |

허브는 두 DB를 **조합**하여 응답한다.  
예: 벡터 검색으로 후보 노드를 추리고 → 그래프 탐색으로 관계를 확인한다.

---

## 2. 전체 파이프라인 흐름

```
[Spoke 요청]
     │
     ▼
[Starcraft Hub — app/ports/input/hub_port.py]  ← 허브의 유일한 진입점
     │
     ├─► [GraphQueryUseCase]  ─────────────────────────────────────────►  [Neo4j]
     │        관계 탐색 · 경로 조회 · 온톨로지 구조 질의 (Cypher)
     │
     ├─► [VectorSearchUseCase]  ───────────────────────────────────────►  [Qdrant]
     │        임베딩 유사도 검색 · 컨텍스트 후보 추출
     │
     └─► [OrchestratorUseCase]  ───────────────────────────────────────►  [Exaone / Gemini]
              그래프 + 벡터 결과를 합쳐 LLM에 컨텍스트로 전달 (RAG)
                    │
                    ▼
           [Spoke 응답 반환]
```

---

## 3. DB 선정

### 3-1. Graph DB — Neo4j

| 항목 | 내용 |
|------|------|
| 선정 이유 | 스타 토폴로지 온톨로지의 허브-스포크 **관계 자체**를 그래프로 저장 |
| 쿼리 언어 | Cypher |
| Python 드라이버 | `neo4j` (공식 비동기 지원) |
| Docker 이미지 | `neo4j:5-community` |
| 기본 포트 | Bolt `7687` / HTTP `7474` |

**저장 모델 예시**

```cypher
// 허브 노드
CREATE (hub:Hub {name: "starcraft", type: "hub"})

// 스포크 노드
CREATE (spoke:Spoke {name: "titanic_m_learning", domain: "ml"})

// 허브-스포크 관계
CREATE (spoke)-[:CONNECTED_TO {weight: 1.0}]->(hub)

// 지식 노드 (온톨로지)
CREATE (concept:Concept {id: "survival_rate", label: "생존율"})
CREATE (spoke)-[:HAS_CONCEPT]->(concept)
```

---

### 3-2. Vector DB — Qdrant

| 항목 | 내용 |
|------|------|
| 선정 이유 | 경량·Docker 친화적, Python SDK 완성도 높음 |
| Python 드라이버 | `qdrant-client` (비동기 지원) |
| Docker 이미지 | `qdrant/qdrant:latest` |
| 기본 포트 | REST `6333` / gRPC `6334` |
| 임베딩 모델 | Exaone(Ollama) 또는 Gemini embedding |

**컬렉션 설계**

```
Collection: "hub_knowledge"
  - vector_size: 768  (임베딩 차원, 모델에 따라 조정)
  - distance: Cosine
  - payload: { spoke: str, concept_id: str, source_md: str, type: "hub"|"spoke" }
```

---

## 4. Docker Compose 추가 전략

현재 `docker-compose.yaml`에 두 서비스를 추가한다.

```yaml
# docker-compose.yaml 에 추가할 서비스

services:
  # ── Graph DB ──────────────────────────────
  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"   # Neo4j Browser (개발 확인용)
      - "7687:7687"   # Bolt 프로토콜 (앱 연결)
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data
    restart: always

  # ── Vector DB ─────────────────────────────
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage
    restart: always

volumes:
  neo4j_data:
  qdrant_data:
```

**환경 변수 (`backend/.env`에 추가)**

```dotenv
# Neo4j
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=hub_knowledge
```

> 로컬 개발 시 `neo4j` → `localhost`, `qdrant` → `localhost`로 변경한다.

---

## 5. 헥사고날 아키텍처 적용

허브 내부는 기존 클린 아키텍처 레이어를 그대로 따른다.

```
starcraft/
├── adapter/
│   ├── inbound/
│   │   └── api/v1/hub_router.py        ← 스포크 요청 수신
│   └── outbound/
│       ├── neo4j/
│       │   └── graph_repository.py     ← Cypher 실행 (Secondary Adapter)
│       └── qdrant/
│           └── vector_repository.py    ← 임베딩 검색 (Secondary Adapter)
├── app/
│   ├── ports/
│   │   ├── input/
│   │   │   └── hub_port.py             ← 스포크가 호출하는 유일한 진입 포트 (ABC)
│   │   └── output/
│   │       ├── graph_port.py           ← Neo4j 포트 (ABC)
│   │       └── vector_port.py          ← Qdrant 포트 (ABC)
│   └── use_cases/
│       ├── graph_query_interactor.py   ← 관계 탐색 유스케이스
│       ├── vector_search_interactor.py ← 벡터 유사도 검색 유스케이스
│       └── orchestrator_interactor.py  ← Graph + Vector + LLM 합성 (RAG)
├── domain/
│   └── entities/
│       ├── hub_node.py                 ← Hub 온톨로지 엔티티
│       └── spoke_node.py               ← Spoke 온톨로지 엔티티
└── dependencies/
    └── hub_provider.py                 ← DIP 조립 (provider 패턴)
```

**의존성 방향 (스타 토폴로지 규칙 유지)**

```
spoke.app.use_cases
    → starcraft.app.ports.input.hub_port  (허브 공개 포트만 참조)
         ↓
    starcraft.app.use_cases.*
         ↓
    starcraft.app.ports.output.graph_port   → Neo4j adapter
    starcraft.app.ports.output.vector_port  → Qdrant adapter
```

---

## 6. RAG 파이프라인 상세

허브의 핵심 역할은 **Graph + Vector → LLM 컨텍스트** 조합이다.

```
1. 스포크가 허브 포트에 질의 전달 (자연어 or 구조화 쿼리)
      │
2. [Vector Search]  질의를 임베딩 → Qdrant에서 Top-K 유사 청크 추출
      │
3. [Graph Query]    추출된 청크의 concept_id로 Neo4j에서 관계 탐색
                    → 연관 스포크·컨셉·경로 확인
      │
4. [컨텍스트 합성]  Vector 결과 + Graph 관계를 프롬프트 컨텍스트로 구성
      │
5. [LLM 호출]       Exaone(로컬) 또는 Gemini(클라우드)에 컨텍스트 전달
      │
6. 스포크에 최종 응답 반환
```

---

## 7. 구현 우선순위

```
1단계  docker-compose.yaml에 neo4j · qdrant 서비스 추가
        → 검증: docker compose up 후 각 DB 포트 접속 확인

2단계  output 포트(ABC) 정의
        graph_port.py · vector_port.py
        → 검증: mypy 통과

3단계  Secondary Adapter 구현
        graph_repository.py (neo4j 드라이버)
        vector_repository.py (qdrant-client)
        → 검증: 각 DB에 샘플 데이터 INSERT · SELECT 테스트 통과

4단계  유스케이스 구현
        graph_query_interactor · vector_search_interactor
        → 검증: pytest 단위 테스트 통과

5단계  orchestrator_interactor (RAG 합성)
        Exaone(FakerOrchestrator) + 위 두 결과 합성
        → 검증: 엔드투엔드 통합 테스트 통과

6단계  hub_router.py (인바운드 어댑터)
        스포크가 호출할 API 엔드포인트 노출
        → 검증: 실제 스포크 하나(titanic_m_learning)와 연동 테스트
```
