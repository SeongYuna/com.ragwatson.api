# Titanic ML — 바운디드 컨텍스트 지침

> 행동 원칙은 루트 `CLAUDE.md`를, 아키텍처·SOLID 규칙은 `backend/CLAUDE.md`를 따른다.

---

## 바운디드 컨텍스트

모듈 루트: `titanic_machine_learning/`  
(`backend/apps/` 는 문서 표기에서 생략한다.)

---

## 참고 구현 경로

### Write (Command — James)

```
titanic_machine_learning/adapter/inbound/api/v1/james_cmd_router.py
  → dependencies/james_provider.py
  → app/use_cases/james_cmd_interactor.py
  → adapter/outbound/repositories/james_cmd_repository.py
```

### Read (Query — Walter)

```
titanic_machine_learning/adapter/inbound/api/v1/walter_query_router.py
  → dependencies/walter_provider.py
  → app/use_cases/walter_query_interactor.py
  → adapter/outbound/repositories/walter_repository.py
```

---

## 도메인 규칙

- DB 규칙(PK `id` 정수 등)은 `backend/_claude/ENTITY_RULES.md`를 따른다.
- Command 경로는 INSERT만, Query 경로는 SELECT만 담당한다.
- 공유 mapper 파일로 Command/Query 경로를 섞지 않는다.

---

## 캐릭터 구현 상태

- Isador, Molly, Ruth: `introduce_myself` 엔드포인트(자기소개)만 구현됨. 실제 유스케이스(승객 조회/통계 등)는 아직 개발 중이며, 각자의 `*_use_case.py` 인터페이스에 메서드를 추가하는 시점부터 확장한다.


## 타이타닉 도메인 문서 연결
* 타이타닉 도메인 문서 연결
* 타이타닉 피쳐 정리 : [[titanic_feature]]
* 타이타닉 머신러닝 :[[titanic_ml_guide]]
* 타이타닉 ERD : [[TITANIC_ERD]]
* 타이타틱 NF : [[titanic_nf]]
* 타이타닉 알고리즘 : [[titanic-algorithm]]`  