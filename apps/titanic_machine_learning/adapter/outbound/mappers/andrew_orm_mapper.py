from titanic_machine_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_machine_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_machine_learning.app.dtos.andrew_dto import (
    AndrewBookingQuery,
    AndrewPassengerQuery,
    AndrewPersonQuery,
)


def person_booking_to_andrew_query(person: PersonORM, booking: BookingORM) -> AndrewPassengerQuery:
    return AndrewPassengerQuery(
        person=AndrewPersonQuery(
            passenger_id=person.passenger_id,
            name=person.name,
            gender=person.gender,
            age=person.age,
            sib_sp=person.sib_sp,
            parch=person.parch,
            survived=person.survived,
        ),
        booking=AndrewBookingQuery(
            pclass=booking.pclass,
            ticket=booking.ticket,
            fare=booking.fare,
            cabin=booking.cabin,
            embarked=booking.embarked,
        ),
    )
