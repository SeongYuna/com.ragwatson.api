from titanic_m_learning.app.dtos.rose_dto import RoseDatasetInfoResult
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.output.rose_repository import RoseRepository
from titanic_m_learning.adapter.inbound.api.schemas.rose_query_schema import RoseIntroduceResponse, RoseIntroduceSchema
from titanic_m_learning.app.dtos.rose_dto import RoseIntroduceQuery


class RoseQueryInteractor(RoseUseCase):
    def __init__(self, repository: RoseRepository) -> None:
        self._repository = repository

    async def get_dataset_info(self) -> RoseDatasetInfoResult:
        return await self._repository.fetch_dataset_info()
    async def introduce_myself(self, schema: RoseIntroduceSchema) -> RoseIntroduceResponse:
        result = await self._repository.introduce_myself(
            RoseIntroduceQuery(id=schema.id, name=schema.name)
        )
        return RoseIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

