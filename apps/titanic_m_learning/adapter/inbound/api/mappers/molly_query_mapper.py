from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyReadNotableSurvivorResponse
from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult, MollyNotableSurvivorQuery
from titanic_m_learning.domain.value_objects.titanic_vo import Gender


def query_to_response(query: MollyNotableSurvivorQuery) -> MollyReadNotableSurvivorResponse:
    return MollyReadNotableSurvivorResponse(
        passenger_id=query.passenger_id,
        name=query.name,
        pclass=query.pclass,
        survived=query.survived,
        gender=Gender.from_sex(query.gender).value,
        assistance_note=query.assistance_note,
    )


def result_to_responses(result: MollyNotableQueryResult) -> list[MollyReadNotableSurvivorResponse]:
    return [query_to_response(query) for query in result.passengers]
