from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AgeBin(str, Enum):
    """나이 구간 — 구간화(binning)로 패턴 단순화."""
    CHILD = "child"      # 0–12
    TEEN = "teen"        # 13–17
    ADULT = "adult"      # 18–60
    SENIOR = "senior"    # 61+
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Age:
    """나이 — 결측값 허용, 구간화 및 교호작용 피처 제공."""

    value: Optional[float]  # None = 결측

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Age":
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            v = float(raw.strip())
            if v < 0:
                raise ValueError(f"Age 음수 불가: '{raw}'")
            return cls(value=v)
        except ValueError:
            raise ValueError(f"Age 유효하지 않은 값: '{raw}'")

    @property
    def is_unknown(self) -> bool:
        return self.value is None

    @property
    def bin(self) -> AgeBin:
        if self.value is None:
            return AgeBin.UNKNOWN
        if self.value <= 12:
            return AgeBin.CHILD
        if self.value <= 17:
            return AgeBin.TEEN
        if self.value <= 60:
            return AgeBin.ADULT
        return AgeBin.SENIOR

    @property
    def is_child(self) -> bool:
        return self.bin == AgeBin.CHILD

    def age_class(self, pclass: int) -> Optional[float]:
        """교호작용 피처: age * pclass"""
        if self.value is None:
            return None
        return self.value * pclass

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "unknown"
