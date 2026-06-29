from titanic_machine_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_machine_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_machine_learning.app.dtos.lowe_dto import LoweLifeboatPassengerQuery


def person_booking_to_lowe_query(person: PersonORM, booking: BookingORM) -> LoweLifeboatPassengerQuery:
    cabin = booking.cabin.strip()
    lifeboat = cabin if cabin else "unknown"
    return LoweLifeboatPassengerQuery(
        passenger_id=person.passenger_id,
        name=person.name,
        lifeboat=lifeboat,
        survived=person.survived,
        gender=person.gender,
        pclass=booking.pclass,
    )
