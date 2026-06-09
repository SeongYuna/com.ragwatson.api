from titanic_m_learning.adapter.inbound.api.schemas.lowe_query_schema import LoweReadLifeboatPassengerResponse
from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatPassengerQuery, LoweLifeboatQueryResult
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: LoweLifeboatPassengerQuery) -> LoweReadLifeboatPassengerResponse:
    return LoweReadLifeboatPassengerResponse(
        passenger_id=query.passenger_id,
        name=query.name,
        lifeboat=query.lifeboat,
        survived=query.survived,
        gender=Gender.from_sex(query.gender).value,
        pclass=query.pclass,
    )


def result_to_responses(result: LoweLifeboatQueryResult) -> list[LoweReadLifeboatPassengerResponse]:
    return [query_to_response(query) for query in result.passengers]
