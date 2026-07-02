from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

    @classmethod
    def from_score(cls, score: float) -> Confidence:
        if score >= 0.85:
            return cls.HIGH
        if score >= 0.60:
            return cls.MEDIUM
        return cls.LOW


@dataclass(frozen=True)
class ClassificationResult:
    is_spam: bool
    category: str
    confidence: Confidence
    score: float
    reasoning: str
