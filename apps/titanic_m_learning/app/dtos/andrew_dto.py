from dataclasses import dataclass


@dataclass(frozen=True)
class AndrewPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class AndrewBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class AndrewPassengerQuery:
    person: AndrewPersonQuery
    booking: AndrewBookingQuery


@dataclass(frozen=True)
class AndrewPageQueryResult:
    passengers: list[AndrewPassengerQuery]
    skip: int
    limit: int
    total: int

@dataclass(frozen=True)
class AndrewIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class AndrewIntroduceResult:
    id: int
    name: str
    message: str
