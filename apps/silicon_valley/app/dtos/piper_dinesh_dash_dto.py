from dataclasses import dataclass


@dataclass(frozen=True)
class PiperDineshDashIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperDineshDashIntroduceResult:
    id: int
    name: str
    message: str
