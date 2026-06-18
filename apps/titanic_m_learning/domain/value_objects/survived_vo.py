from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Survived:
    """생존 여부 — 타겟 변수. 0=사망, 1=생존."""

    value: bool

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Survived":
        if raw is None or raw.strip() == "":
            raise ValueError("Survived는 필수 값입니다.")
        stripped = raw.strip()
        if stripped == "1":
            return cls(value=True)
        if stripped == "0":
            return cls(value=False)
        raise ValueError(f"Survived 유효하지 않은 값: '{raw}'")

    @property
    def is_survived(self) -> bool:
        return self.value

    def to_int(self) -> int:
        return 1 if self.value else 0

    def __str__(self) -> str:
        return "생존" if self.value else "사망"
