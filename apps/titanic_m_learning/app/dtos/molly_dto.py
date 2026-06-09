from dataclasses import dataclass


@dataclass(frozen=True)
class MollyNotableSurvivorQuery:
    passenger_id: str
    name: str
    pclass: str
    survived: str
    gender: str
    assistance_note: str


@dataclass(frozen=True)
class MollyNotableQueryResult:
    passengers: list[MollyNotableSurvivorQuery]

@dataclass(frozen=True)
class MollyIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class MollyIntroduceResult:
    id: int
    name: str
    message: str
