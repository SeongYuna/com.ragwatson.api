from dataclasses import dataclass


@dataclass(frozen=True)
class LoweLifeboatPassengerQuery:
    passenger_id: str
    name: str
    lifeboat: str
    survived: str
    gender: str
    pclass: str


@dataclass(frozen=True)
class LoweLifeboatQueryResult:
    passengers: list[LoweLifeboatPassengerQuery]

@dataclass(frozen=True)
class LoweIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class LoweIntroduceResult:
    id: int
    name: str
    message: str
