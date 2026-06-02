from titanic_m_learning.adapter.outbound.orm.titanic_orm import TitanicPassengerORM
from titanic_m_learning.app.dtos.james_cmd_dto import JamesPassengerCommand
from titanic_m_learning.domain.entities.titanic import TitanicPassenger
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def command_to_orm(command: JamesPassengerCommand) -> TitanicPassengerORM:
    person = command.person
    booking = command.booking
    return TitanicPassengerORM(
        passenger_id=person.passenger_id,
        survived=person.survived,
        pclass=booking.pclass,
        name=person.name,
        gender=Gender.from_sex(person.gender).value,
        age=person.age,
        sib_sp=person.sib_sp,
        parch=person.parch,
        ticket=booking.ticket,
        fare=booking.fare,
        cabin=booking.cabin,
        embarked=booking.embarked,
    )


def orm_to_passenger(row: TitanicPassengerORM) -> TitanicPassenger:
    return TitanicPassenger.from_persistence(
        passenger_id=row.passenger_id,
        survived=row.survived,
        pclass=row.pclass,
        name=row.name,
        gender=row.gender,
        age=row.age,
        sib_sp=row.sib_sp,
        parch=row.parch,
        ticket=row.ticket,
        fare=row.fare,
        cabin=row.cabin,
        embarked=row.embarked,
    )


def passenger_to_orm(passenger: TitanicPassenger) -> TitanicPassengerORM:
    return TitanicPassengerORM(
        passenger_id=passenger.passenger_id,
        survived=passenger.survived,
        pclass=passenger.pclass,
        name=passenger.name,
        gender=passenger.gender.value,
        age=passenger.age,
        sib_sp=passenger.sib_sp,
        parch=passenger.parch,
        ticket=passenger.ticket,
        fare=passenger.fare,
        cabin=passenger.cabin,
        embarked=passenger.embarked,
    )
