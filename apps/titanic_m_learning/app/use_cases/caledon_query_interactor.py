from titanic_m_learning.app.dtos.caledon_dto import CaledonStatsResult
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.output.caledon_repository import CaledonRepository
from titanic_m_learning.adapter.inbound.api.schemas.cal_query_schema import CaledonIntroduceResponse, CaledonIntroduceSchema
from titanic_m_learning.app.dtos.caledon_dto import CaledonIntroduceQuery


class CaledonQueryInteractor(CaledonUseCase):
    def __init__(self, repository: CaledonRepository) -> None:
        self._repository = repository

    async def calculate_stats(self) -> CaledonStatsResult:
        return await self._repository.fetch_stats()
    async def introduce_myself(self, schema: CaledonIntroduceSchema) -> CaledonIntroduceResponse:
        result = await self._repository.introduce_myself(
            CaledonIntroduceQuery(id=schema.id, name=schema.name)
        )
        return CaledonIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

