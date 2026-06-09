from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase
from titanic_m_learning.app.ports.output.smith_repository import SmithRepository
from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import SmithIntroduceResponse, SmithIntroduceSchema
from titanic_m_learning.app.dtos.smith_dto import SmithIntroduceQuery


class SmithQueryInteractor(SmithUseCase):
    def __init__(self, repository: SmithRepository) -> None:
        self._repository = repository

    async def get_summary(self) -> SmithStatsResult:
        return await self._repository.fetch_summary()
    async def introduce_myself(self, schema: SmithIntroduceSchema) -> SmithIntroduceResponse:
        result = await self._repository.introduce_myself(
            SmithIntroduceQuery(id=schema.id, name=schema.name)
        )
        return SmithIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

