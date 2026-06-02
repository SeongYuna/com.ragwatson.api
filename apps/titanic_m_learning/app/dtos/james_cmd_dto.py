from dataclasses import dataclass


@dataclass(frozen=True)
class PersonCommand:
    """Person 역정규화 커맨드. 모든 필드는 str."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class BookingCommand:
    """Booking + Port(Country 제외) 역정규화 커맨드. 모든 필드는 str."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class JamesPassengerCommand:
    """CSV 1행 = PersonCommand + BookingCommand."""

    person: PersonCommand
    booking: BookingCommand
