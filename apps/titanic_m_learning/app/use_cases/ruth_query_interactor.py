from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_m_learning.app.ports.output.ruth_repository import RuthRepository
from titanic_m_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthIntroduceResponse, RuthIntroduceSchema
from titanic_m_learning.app.dtos.ruth_dto import RuthIntroduceQuery


class RuthQueryInteractor(RuthUseCase):
    def __init__(self, repository: RuthRepository) -> None:
        self._repository = repository

    async def introduce_myself(self, schema: RuthIntroduceSchema) -> RuthIntroduceResponse:
        result = await self._repository.introduce_myself(
            RuthIntroduceQuery(id=schema.id, name=schema.name)
        )
        return RuthIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )
