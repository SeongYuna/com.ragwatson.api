from titanic_m_learning.adapter.inbound.api.schemas.walter_query_schema import WalterReadPassengerResponse
from titanic_m_learning.app.dtos.walter_dto import WalterPassengerQuery, WalterTableQueryResult
from titanic_m_learning.domain.value_objects.gender_vo import Gender


def query_to_response(query: WalterPassengerQuery) -> WalterReadPassengerResponse:
    person = query.person
    booking = query.booking
    return WalterReadPassengerResponse(
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


def queries_to_responses(queries: list[WalterPassengerQuery]) -> list[WalterReadPassengerResponse]:
    return [query_to_response(query) for query in queries]


def table_result_to_responses(result: WalterTableQueryResult) -> list[WalterReadPassengerResponse]:
    return queries_to_responses(result.passengers)
