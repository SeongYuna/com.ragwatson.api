from dataclasses import dataclass


@dataclass(frozen=True)
class IsadorPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class IsadorBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class IsadorPassengerQuery:
    person: IsadorPersonQuery
    booking: IsadorBookingQuery

@dataclass(frozen=True)
class IsadorIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class IsadorIntroduceResult:
    id: int
    name: str
    message: str
