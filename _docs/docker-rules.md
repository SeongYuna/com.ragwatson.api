<!--
# Docker 컨테이너 생성 규칙

> Cursor / AI 에이전트용. DB·백엔드 컨테이너를 새로 띄우거나 `docker run` / `docker compose up`을 실행하기 전 **이 문서를 따른다.**

---

## 1. 배경 (2026-07-16 정리)

수동으로 반복 생성된 컨테이너가 `docker-compose.yaml`이 관리하는 서비스와 중복되어 있었다. 아래 컨테이너를 중복으로 판단해 제거했다.

| 컨테이너 | 대응하는 compose 서비스 |
|----------|--------------------------|
| `thomas-watson-backend` | `my-backend` |
| `redis:7-alpine` | `redis` |
| `pgvector/pgvector:pg17` | `pgvector` |
| `n8nio/n8n:latest` | `n8n` |
| `neo4j:5` | `neo4j` |

정식 서비스 정의는 msa 루트 저장소(`com.ragwatson`)의 `docker-compose.yaml`(프로덕션) / `docker-compose.dev.yaml`(개발) 하나뿐이며(backend 저장소 자체에는 없음), 동일 역할의 컨테이너를 compose 밖에서 별도로 `docker run`하지 않는다.

---

## 2. 기본 원칙 (필수)

- 새 DB·백엔드 컨테이너가 필요하다는 요청을 받으면, **먼저 기존 컨테이너·서비스가 있는지 확인**한다.
  ```bash
  docker ps -a
  docker compose ps
  ```
- 동일 역할(같은 이미지·같은 포트·같은 목적)의 컨테이너가 **이미 있으면**:
  - 임의로 새로 만들지 않는다.
  - 기존 것을 재사용할지, 교체(재생성)할지 **사용자에게 확인받는다.**
- 승인 없이 중복 컨테이너를 생성하지 않는다.
- 새 서비스가 정말 필요하면 `docker-compose.yaml`(필요 시 `docker-compose.dev.yaml`)에 **서비스로 등록**한다. compose 밖에서 개별 `docker run`으로 관리하지 않는다.

---

## 3. 체크리스트

- [ ] `docker ps -a` / `docker compose ps`로 기존 컨테이너를 확인했는가?
- [ ] 동일 역할의 기존 컨테이너·서비스가 있는가? 있다면 사용자 승인을 받았는가?
- [ ] 신규 서비스는 `docker-compose.yaml`에 등록했는가 (compose 밖 `docker run` 아님)?

---

## 4. 에이전트 지시 (복사용)

```text
@backend/_docs/docker-rules.md 를 따르세요.
DB·백엔드 컨테이너를 새로 생성하기 전에 기존 컨테이너(docker ps -a, docker compose ps)를 먼저 확인하고,
동일 역할의 것이 이미 있으면 임의로 새로 만들지 말고 재사용/교체 여부를 승인받으세요.
```
-->
