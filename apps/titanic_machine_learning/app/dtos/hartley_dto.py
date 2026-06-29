from dataclasses import dataclass


@dataclass(frozen=True)
class HartleyPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class HartleyBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class HartleyPassengerQuery:
    person: HartleyPersonQuery
    booking: HartleyBookingQuery

@dataclass(frozen=True)
class HartleyIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class HartleyIntroduceResult:
    id: int
    name: str
    message: str
