from titanic_m_learning.app.dtos.hartley_dto import HartleyPassengerQuery
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.hartley_repository import HartleyRepository
from titanic_m_learning.adapter.inbound.api.schemas.hartley_query_schema import HartleyIntroduceResponse, HartleyIntroduceSchema
from titanic_m_learning.app.dtos.hartley_dto import HartleyIntroduceQuery


class HartleyQueryInteractor(HartleyUseCase):
    def __init__(self, repository: HartleyRepository) -> None:
        self._repository = repository

    async def sample(self, *, count: int = 10) -> list[HartleyPassengerQuery]:
        return await self._repository.sample(count=count)
    async def introduce_myself(self, schema: HartleyIntroduceSchema) -> HartleyIntroduceResponse:
        result = await self._repository.introduce_myself(
            HartleyIntroduceQuery(id=schema.id, name=schema.name)
        )
        return HartleyIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

