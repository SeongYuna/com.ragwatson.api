from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.walter_dto import (
    BookingQuery,
    PersonQuery,
    WalterPassengerQuery,
)


def orm_to_person_query(person: PersonORM) -> PersonQuery:
    return PersonQuery(
        passenger_id=person.passenger_id,
        name=person.name,
        gender=person.gender,
        age=person.age,
        sib_sp=person.sib_sp,
        parch=person.parch,
        survived=person.survived,
    )


def orm_to_booking_query(booking: BookingORM) -> BookingQuery:
    return BookingQuery(
        pclass=booking.pclass,
        ticket=booking.ticket,
        fare=booking.fare,
        cabin=booking.cabin,
        embarked=booking.embarked,
    )


def person_booking_to_query(person: PersonORM, booking: BookingORM) -> WalterPassengerQuery:
    return WalterPassengerQuery(
        person=orm_to_person_query(person),
        booking=orm_to_booking_query(booking),
    )
