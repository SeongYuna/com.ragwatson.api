from titanic_m_learning.app.dtos.jack_dto import JackPassengerQuery
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.output.jack_repository import JackRepository
from titanic_m_learning.adapter.inbound.api.schemas.jack_query_schema import JackIntroduceResponse, JackIntroduceSchema
from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery


class JackQueryInteractor(JackUseCase):
    def __init__(self, repository: JackRepository) -> None:
        self._repository = repository

    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        return await self._repository.find_by_id(passenger_id)
    async def introduce_myself(self, schema: JackIntroduceSchema) -> JackIntroduceResponse:
        result = await self._repository.introduce_myself(
            JackIntroduceQuery(id=schema.id, name=schema.name)
        )
        return JackIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

