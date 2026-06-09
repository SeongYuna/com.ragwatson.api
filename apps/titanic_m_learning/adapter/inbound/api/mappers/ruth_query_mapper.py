from titanic_m_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthReadPassengerResponse
from titanic_m_learning.app.dtos.ruth_dto import RuthPassengerQuery
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: RuthPassengerQuery) -> RuthReadPassengerResponse:
    person = query.person
    booking = query.booking
    return RuthReadPassengerResponse(
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


def queries_to_responses(queries: list[RuthPassengerQuery]) -> list[RuthReadPassengerResponse]:
    return [query_to_response(query) for query in queries]
