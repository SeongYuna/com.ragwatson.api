# Titanic ML — 바운디드 컨텍스트 지침

> 행동 원칙은 루트 `CLAUDE.md`를, 아키텍처·SOLID 규칙은 `backend/CLAUDE.md`를 따른다.

---

## 바운디드 컨텍스트

모듈 루트: `titanic_m_learning/`  
(`backend/apps/` 는 문서 표기에서 생략한다.)

---

## 참고 구현 경로

### Write (Command — James)

```
titanic_m_learning/adapter/inbound/api/v1/james_cmd_router.py
  → dependencies/james_provider.py
  → app/use_cases/james_cmd_interactor.py
  → adapter/outbound/pg/james_cmd_pg_repository.py
```

### Read (Query — Walter)

```
titanic_m_learning/adapter/inbound/api/v1/walter_query_router.py
  → dependencies/walter_provider.py
  → app/use_cases/walter_query_interactor.py
  → adapter/outbound/pg/walter_pg_repository.py
```

---

## 도메인 규칙

- DB 규칙(PK `id` 정수 등)은 `docs/AIOPS/backend/entity_rules.md`를 따른다.
- Command 경로는 INSERT만, Query 경로는 SELECT만 담당한다.
- 공유 mapper 파일로 Command/Query 경로를 섞지 않는다.


## 타이타닉 도메인 문서 연결
* 타이타닉 도메인 문서 연결
* 타이타닉 피쳐 정리 : [[titanic_feature]]
* 타이타닉 머신러닝 :[[titanic_ml_guide]]
* 타이타닉 ERD : [[TITANIC_ERD]]
* 타이타틱 NF : [[titanic_nf]]
* 타이타닉 알고리즘 : [[titanic-algorithm]]`  