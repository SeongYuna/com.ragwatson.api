from dataclasses import dataclass


@dataclass(frozen=True)
class CaledonStatsResult:
    total: int
    survived: int
    deceased: int
    survival_rate: float

@dataclass(frozen=True)
class CaledonModelScore:
    algorithm: str
    accuracy: float
    precision: float
    recall: float
    f1: float


@dataclass(frozen=True)
class CaledonModelTestResult:
    scores: tuple[CaledonModelScore, ...]
    winner: str          # 정확도 1위 알고리즘 이름
    winner_accuracy: float


@dataclass(frozen=True)
class CaledonIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class CaledonIntroduceResult:
    id: int
    name: str
    message: str
