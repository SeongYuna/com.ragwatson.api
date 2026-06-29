from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class FamilyProfile:
    """SibSp + Parch를 하나의 임베디드 값 타입으로 캡슐화.

    sibsp·parch는 상호 상관(0.25)이 높고,
    파생 지표인 FamilySize(sibsp+parch)와 Alone은 각각 0.75·0.63 이상의
    내부 상관을 가지므로 단일 VO로 관리한다.

    Survived 상관: sibsp=+0.10 / alone=-0.11 (동반자 있을수록 생존 유리)
    """

    sibsp: int
    parch: int

    @classmethod
    def from_raw(cls, sibsp_raw: Optional[str], parch_raw: Optional[str]) -> "FamilyProfile":
        def _parse(val: Optional[str], name: str) -> int:
            if val is None or val.strip() == "":
                raise ValueError(f"{name}는 필수 값입니다.")
            try:
                v = int(val.strip())
            except ValueError:
                raise ValueError(f"{name} 유효하지 않은 값: '{val}'")
            if v < 0:
                raise ValueError(f"{name} 음수 불가: '{val}'")
            return v

        return cls(
            sibsp=_parse(sibsp_raw, "SibSp"),
            parch=_parse(parch_raw, "Parch"),
        )

    @property
    def size(self) -> int:
        """동반 가족 수 (본인 제외)."""
        return self.sibsp + self.parch

    @property
    def is_alone(self) -> bool:
        """단독 탑승 여부."""
        return self.size == 0

    @property
    def is_small(self) -> bool:
        """소규모 동반 (1~3명) — 생존율 비교적 높음."""
        return 1 <= self.size <= 3

    @property
    def is_large(self) -> bool:
        """대가족 동반 (4명 이상) — 생존율 낮을 수 있음."""
        return self.size >= 4

    def to_sibsp_int(self) -> int:
        return self.sibsp

    def to_parch_int(self) -> int:
        return self.parch

    def to_size_int(self) -> int:
        return self.size

    def to_alone_int(self) -> int:
        return int(self.is_alone)

    def __str__(self) -> str:
        tag = "alone" if self.is_alone else f"family({self.size})"
        return tag
