from titanic_m_learning.adapter.inbound.api.schemas.andrew_query_schema import AndrewReadPassengerResponse
from titanic_m_learning.app.dtos.andrew_dto import AndrewPassengerQuery
from titanic_m_learning.domain.value_objects.gender_vo import Gender


def query_to_response(query: AndrewPassengerQuery) -> AndrewReadPassengerResponse:
    person = query.person
    booking = query.booking
    return AndrewReadPassengerResponse(
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


def queries_to_responses(queries: list[AndrewPassengerQuery]) -> list[AndrewReadPassengerResponse]:
    return [query_to_response(query) for query in queries]
