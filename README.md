# seongyuna.cloud

개인 워크스페이스이자, **LLM 코딩 에이전트를 하네스(안전대·고삐)로 묶는** 규범과 메모를 두는 저장소다.

## 왜 이 구조인가 (하네스 + 카파시)

[안드레이 카파시(Andrej Karpathy)](https://x.com/karpathy/status/2015883857489522876)는 모델이 **잘못된 가정을 확인 없이 밀고 가고**, **과설계**하며, **과제와 무관한 코드**까지 건드리는 경향을 지적했다. 이를 막으려면 프롬프트만으로는 부족하고, **규칙·문서·검증 루프**로 행동을 고정하는 **하네스 엔지니어링**이 필요하다.

카파시가 강조한 것처럼, 모델은 **구체적인 성공 기준**이 있을 때 반복·수정에 강하다. 그래서 이 저장소는 네 가지 축—**구현 전 사고**, **단순성 우선**, **정밀한 수정**, **목표 중심 실행**—을 문서로 고정해 두었다. (정리 예시: [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills))

## 문서 한눈에 보기

| 파일 | 역할 |
|------|------|
| [`CLAUDE.md`](./CLAUDE.md) | 에이전트 **행동 규범** 전문. 카파시가 짚은 실패 모드, 네 원칙, 인용·표·체크리스트. |
| [`.cursorrules`](./.cursorrules) | Cursor에 매번 실리는 **짧은 고삐**. `CLAUDE.md`와 같은 축을 압축. |
| [`CURSOR.md`](./CURSOR.md) | Cursor 안에서 **하네스를 쌓는 방법**—규칙 디렉터리, User Rules, 스킬, CI와의 맞물림. |

프로젝트별로 더 쪼개고 싶으면 `.cursor/rules/`에 경로·금지 사항·완료 조건을 추가하면 된다. 자세한 권장 배치는 `CURSOR.md`를 본다.

## 쓰는 법

1. 에이전트에게 작업을 줄 때 **완료 정의**를 붙인다. (테스트 통과, 린트 무경고 등.)
2. `CLAUDE.md`와 `.cursorrules`는 저장소 루트에 두어 **항상 같은 규범**이 오가게 한다.
3. 팀·다른 저장소로 복사할 때는 `CLAUDE.md`를 베이스로 **프로젝트 전용 절**만 아래에 합친다.

## 그 밖의 경로

- `docs/` — Obsidian 등으로 관리하는 메모·기획 문서.

## 출처

카파시 관찰·네 원칙 정리본을 인용·재배포할 때는 [해당 트윗](https://x.com/karpathy/status/2015883857489522876)과 [andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) 출처를 밝히는 것을 권장한다.
