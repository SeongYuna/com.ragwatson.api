from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.james_cmd_dto import JamesPassengerCommand


def command_to_person_orm(command: JamesPassengerCommand) -> PersonORM:
    person = command.person
    return PersonORM(
        passenger_id=person.passenger_id,
        name=person.name,
        gender=person.gender,
        age=person.age,
        sib_sp=person.sib_sp,
        parch=person.parch,
        survived=person.survived,
    )


def command_to_booking_orm(command: JamesPassengerCommand) -> BookingORM:
    booking = command.booking
    return BookingORM(
        passenger_id=command.person.passenger_id,
        pclass=booking.pclass,
        ticket=booking.ticket,
        fare=booking.fare,
        cabin=booking.cabin,
        embarked=booking.embarked,
    )
