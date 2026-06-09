from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatQueryResult
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.output.lowe_repository import LoweRepository
from titanic_m_learning.adapter.inbound.api.schemas.lowe_query_schema import LoweIntroduceResponse, LoweIntroduceSchema
from titanic_m_learning.app.dtos.lowe_dto import LoweIntroduceQuery


class LoweQueryInteractor(LoweUseCase):
    def __init__(self, repository: LoweRepository) -> None:
        self._repository = repository

    async def find_lifeboats(
        self,
        *,
        lifeboat: str | None = None,
    ) -> LoweLifeboatQueryResult:
        return await self._repository.find_lifeboats(lifeboat=lifeboat)
    async def introduce_myself(self, schema: LoweIntroduceSchema) -> LoweIntroduceResponse:
        result = await self._repository.introduce_myself(
            LoweIntroduceQuery(id=schema.id, name=schema.name)
        )
        return LoweIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

