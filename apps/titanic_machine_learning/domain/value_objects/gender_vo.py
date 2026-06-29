from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Gender:
    """성별 — "여성과 어린이 우선" 원칙으로 생존에 가장 강력한 변수."""

    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        if raw is None or raw.strip() == "":
            return cls(value=GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        try:
            return cls(value=GenderType(normalized))
        except ValueError:
            raise ValueError(f"Gender 유효하지 않은 값: '{raw}'")

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    @property
    def is_unknown(self) -> bool:
        return self.value == GenderType.UNKNOWN

    def to_int(self) -> int:
        """ML 인코딩: female=1, male=0, unknown=-1"""
        return {GenderType.FEMALE: 1, GenderType.MALE: 0, GenderType.UNKNOWN: -1}[self.value]

    def __str__(self) -> str:
        return self.value.value
