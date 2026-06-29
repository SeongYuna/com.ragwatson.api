from dataclasses import dataclass


@dataclass(frozen=True)
class MollyIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MollyIntroduceResult:
    id: int
    name: str
    message: str
