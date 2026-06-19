from dataclasses import dataclass


@dataclass(frozen=True)
class PiperDunnCooIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperDunnCooIntroduceResult:
    id: int
    name: str
    message: str
