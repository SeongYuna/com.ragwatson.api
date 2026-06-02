from dataclasses import dataclass


@dataclass(frozen=True)
class StatsResult:
    total: int
    survived: int
    deceased: int
    survival_rate: float
