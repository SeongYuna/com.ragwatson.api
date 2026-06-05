from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.dtos.table_query_result import TableQueryResult
from titanic_m_learning.app.dtos.walter_dto import WalterPassengerQuery
from titanic_m_learning.domain.entities.titanic import TitanicPassenger
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: WalterPassengerQuery) -> TitanicPassengerResponse:
    person = query.person
    booking = query.booking
    return TitanicPassengerResponse(
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


def queries_to_responses(queries: list[WalterPassengerQuery]) -> list[TitanicPassengerResponse]:
    return [query_to_response(query) for query in queries]


def table_result_to_responses(result: TableQueryResult) -> list[TitanicPassengerResponse]:
    return queries_to_responses(result.passengers)


def passenger_to_response(passenger: TitanicPassenger) -> TitanicPassengerResponse:
    return TitanicPassengerResponse(
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


def passengers_to_responses(
    passengers: list[TitanicPassenger],
) -> list[TitanicPassengerResponse]:
    return [passenger_to_response(p) for p in passengers]
