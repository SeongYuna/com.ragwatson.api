from dataclasses import dataclass


@dataclass(frozen=True)
class PiperBighettiHrIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperBighettiHrIntroduceResult:
    id: int
    name: str
    message: str
