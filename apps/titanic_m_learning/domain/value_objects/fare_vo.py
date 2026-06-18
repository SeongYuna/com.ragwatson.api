from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Fare:
    """운임 요금 — 연속형, 왜도 완화를 위한 로그 변환 제공."""

    value: Optional[float]  # None = 결측 (테스트셋 1개)

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Fare":
        if raw is None or raw.strip() == "":
            return cls(value=None)
        try:
            v = float(raw.strip())
            if v < 0:
                raise ValueError(f"Fare 음수 불가: '{raw}'")
            return cls(value=v)
        except ValueError:
            raise ValueError(f"Fare 유효하지 않은 값: '{raw}'")

    @property
    def is_missing(self) -> bool:
        return self.value is None

    @property
    def log_scaled(self) -> Optional[float]:
        """log1p 변환으로 왜도(skewness) 완화."""
        if self.value is None:
            return None
        return math.log1p(self.value)

    def per_person(self, family_size: int) -> Optional[float]:
        """실질 지불 운임 추정: fare / family_size"""
        if self.value is None or family_size <= 0:
            return None
        return self.value / family_size

    def __str__(self) -> str:
        return str(self.value) if self.value is not None else "unknown"
