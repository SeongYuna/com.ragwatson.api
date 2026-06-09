from dataclasses import dataclass


@dataclass(frozen=True)
class JackPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class JackBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class JackPassengerQuery:
    person: JackPersonQuery
    booking: JackBookingQuery

@dataclass(frozen=True)
class JackIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JackIntroduceResult:
    id: int
    name: str
    message: str
