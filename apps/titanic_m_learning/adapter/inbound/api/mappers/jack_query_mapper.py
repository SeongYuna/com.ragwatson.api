from titanic_m_learning.adapter.inbound.api.schemas.jack_query_schema import JackReadPassengerResponse
from titanic_m_learning.app.dtos.jack_dto import JackPassengerQuery
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: JackPassengerQuery) -> JackReadPassengerResponse:
    person = query.person
    booking = query.booking
    return JackReadPassengerResponse(
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
