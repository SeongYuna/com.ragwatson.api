from dataclasses import dataclass


@dataclass(frozen=True)
class RuthPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class RuthBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class RuthPassengerQuery:
    person: RuthPersonQuery
    booking: RuthBookingQuery

@dataclass(frozen=True)
class RuthIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RuthIntroduceResult:
    id: int
    name: str
    message: str
