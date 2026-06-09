from dataclasses import dataclass


@dataclass(frozen=True)
class WalterPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class WalterBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class WalterPassengerQuery:
    person: WalterPersonQuery
    booking: WalterBookingQuery


@dataclass(frozen=True)
class WalterTableQueryResult:
    passengers: list[WalterPassengerQuery]

    @property
    def count(self) -> int:
        return len(self.passengers)

@dataclass(frozen=True)
class WalterIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class WalterIntroduceResult:
    id: int
    name: str
    message: str
