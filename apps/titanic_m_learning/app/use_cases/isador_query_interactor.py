from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.ports.output.isador_repository import IsadorRepository
from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorIntroduceResponse, IsadorIntroduceSchema
from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery


class IsadorQueryInteractor(IsadorUseCase):
    def __init__(self, repository: IsadorRepository) -> None:
        self._repository = repository

    async def find_families(self) -> list[IsadorPassengerQuery]:
        return await self._repository.find_families()
    async def introduce_myself(self, schema: IsadorIntroduceSchema) -> IsadorIntroduceResponse:
        result = await self._repository.introduce_myself(
            IsadorIntroduceQuery(id=schema.id, name=schema.name)
        )
        return IsadorIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

