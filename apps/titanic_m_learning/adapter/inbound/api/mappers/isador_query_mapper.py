from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorReadPassengerResponse
from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: IsadorPassengerQuery) -> IsadorReadPassengerResponse:
    person = query.person
    booking = query.booking
    return IsadorReadPassengerResponse(
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


def queries_to_responses(queries: list[IsadorPassengerQuery]) -> list[IsadorReadPassengerResponse]:
    return [query_to_response(query) for query in queries]
