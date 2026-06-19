from titanic_m_learning.adapter.inbound.api.schemas.hartley_query_schema import HartleyReadPassengerResponse
from titanic_m_learning.app.dtos.hartley_dto import HartleyPassengerQuery
from titanic_m_learning.domain.value_objects.gender_vo import Gender


def query_to_response(query: HartleyPassengerQuery) -> HartleyReadPassengerResponse:
    person = query.person
    booking = query.booking
    return HartleyReadPassengerResponse(
        passenger_id=person.passenger_id,
        survived=person.survived,
        pclass=booking.pclass,
        name=person.name,
        gender=Gender.from_raw(person.gender).value,
        age=person.age,
        sib_sp=person.sib_sp,
        parch=person.parch,
        ticket=booking.ticket,
        fare=booking.fare,
        cabin=booking.cabin,
        embarked=booking.embarked,
    )


def queries_to_responses(queries: list[HartleyPassengerQuery]) -> list[HartleyReadPassengerResponse]:
    return [query_to_response(query) for query in queries]
