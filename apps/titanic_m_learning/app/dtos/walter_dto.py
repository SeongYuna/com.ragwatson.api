from dataclasses import dataclass


@dataclass(frozen=True)
class PersonQuery:
    """Person 역정규화 조회 DTO. 모든 필드는 str."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class BookingQuery:
    """Booking + Port(Country 제외) 역정규화 조회 DTO. 모든 필드는 str."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class WalterPassengerQuery:
    """DB 1행 = PersonQuery + BookingQuery."""

    person: PersonQuery
    booking: BookingQuery
