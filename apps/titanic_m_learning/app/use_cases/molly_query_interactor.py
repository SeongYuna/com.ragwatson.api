from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult
from titanic_m_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_m_learning.app.ports.output.molly_repository import MollyRepository
from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyIntroduceResponse, MollyIntroduceSchema
from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery


class MollyQueryInteractor(MollyUseCase):
    def __init__(self, repository: MollyRepository) -> None:
        self._repository = repository

    async def find_notable(self) -> MollyNotableQueryResult:
        return await self._repository.find_notable()
    async def introduce_myself(self, schema: MollyIntroduceSchema) -> MollyIntroduceResponse:
        result = await self._repository.introduce_myself(
            MollyIntroduceQuery(id=schema.id, name=schema.name)
        )
        return MollyIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

