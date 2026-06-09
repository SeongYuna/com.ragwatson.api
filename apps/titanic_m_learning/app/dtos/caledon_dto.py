from dataclasses import dataclass


@dataclass(frozen=True)
class CaledonStatsResult:
    total: int
    survived: int
    deceased: int
    survival_rate: float

@dataclass(frozen=True)
class CaledonIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class CaledonIntroduceResult:
    id: int
    name: str
    message: str
