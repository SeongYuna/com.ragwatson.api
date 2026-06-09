from titanic_m_learning.app.dtos.walter_dto import WalterTableQueryResult
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository
from titanic_m_learning.adapter.inbound.api.schemas.walter_query_schema import WalterIntroduceResponse, WalterIntroduceSchema
from titanic_m_learning.app.dtos.walter_dto import WalterIntroduceQuery


class WalterQueryInteractor(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def find_all(self) -> WalterTableQueryResult:
        queries = await self._repository.find_all()
        return WalterTableQueryResult(passengers=queries)
    async def introduce_myself(self, schema: WalterIntroduceSchema) -> WalterIntroduceResponse:
        result = await self._repository.introduce_myself(
            WalterIntroduceQuery(id=schema.id, name=schema.name)
        )
        return WalterIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

