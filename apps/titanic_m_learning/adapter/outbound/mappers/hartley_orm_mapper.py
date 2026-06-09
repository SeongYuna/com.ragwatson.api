from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.hartley_dto import (
    HartleyBookingQuery,
    HartleyPassengerQuery,
    HartleyPersonQuery,
)


def person_booking_to_hartley_query(person: PersonORM, booking: BookingORM) -> HartleyPassengerQuery:
    return HartleyPassengerQuery(
        person=HartleyPersonQuery(
            passenger_id=person.passenger_id,
            name=person.name,
            gender=person.gender,
            age=person.age,
            sib_sp=person.sib_sp,
            parch=person.parch,
            survived=person.survived,
        ),
        booking=HartleyBookingQuery(
            pclass=booking.pclass,
            ticket=booking.ticket,
            fare=booking.fare,
            cabin=booking.cabin,
            embarked=booking.embarked,
        ),
    )
