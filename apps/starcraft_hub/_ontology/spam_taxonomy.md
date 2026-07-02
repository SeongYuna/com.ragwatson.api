---
type: ontology-taxonomy
domain: spam-classification
---

# 스팸 분류 온톨로지 (Spam Classification Ontology)

## 최상위 개념 (Top Concepts)

- **Email** — 분류 대상 이메일 엔티티
- **SpamCategory** — 스팸 유형 분류 노드
- **LegitimateCategory** — 정상 메일 유형 분류 노드

## SpamCategory 계층

```
SpamCategory
├── Phishing          # 피싱 (계정 탈취, 가짜 로그인 유도)
├── Advertising       # 광고 (무단 마케팅, 홍보)
├── Malware           # 악성코드 링크/첨부파일 포함
├── Scam              # 사기 (투자 사기, 복권 당첨 등)
└── SocialEngineering # 사회공학 (긴급 요청, 신뢰 조작)
```

## LegitimateCategory 계층

```
LegitimateCategory
├── Transactional     # 거래 확인, 영수증, 배송 알림
├── Newsletter        # 구독 뉴스레터
├── Personal          # 개인 간 메일
└── Work              # 업무 메일
```

## 관계 (Relations)

| 관계명 | 주어 | 목적어 | 설명 |
|--------|------|--------|------|
| `hasCategory` | Email | SpamCategory / LegitimateCategory | 이메일의 분류 |
| `subClassOf` | 하위 카테고리 | 상위 카테고리 | 계층 관계 |
| `indicatedBy` | SpamCategory | Keyword | 분류 근거 키워드 |
| `triggeredBy` | SpamCategory | Pattern | 분류 근거 패턴 |

## 분류 신뢰도 (Confidence)

- `HIGH` ≥ 0.85
- `MEDIUM` 0.60 – 0.84
- `LOW` < 0.60
