from dataclasses import dataclass


@dataclass(frozen=True)
class RuthIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RuthIntroduceResult:
    id: int
    name: str
    message: str
