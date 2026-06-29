from titanic_machine_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_machine_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_machine_learning.app.dtos.jack_dto import JackBookingQuery, JackPassengerQuery, JackPersonQuery


def person_booking_to_jack_query(person: PersonORM, booking: BookingORM) -> JackPassengerQuery:
    return JackPassengerQuery(
        person=JackPersonQuery(
            passenger_id=person.passenger_id,
            name=person.name,
            gender=person.gender,
            age=person.age,
            sib_sp=person.sib_sp,
            parch=person.parch,
            survived=person.survived,
        ),
        booking=JackBookingQuery(
            pclass=booking.pclass,
            ticket=booking.ticket,
            fare=booking.fare,
            cabin=booking.cabin,
            embarked=booking.embarked,
        ),
    )
