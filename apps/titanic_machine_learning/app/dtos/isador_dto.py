from dataclasses import dataclass


@dataclass(frozen=True)
class IsadorIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class IsadorIntroduceResult:
    id: int
    name: str
    message: str
