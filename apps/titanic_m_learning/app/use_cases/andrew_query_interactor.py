from titanic_m_learning.app.dtos.andrew_dto import AndrewPageQueryResult
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.app.ports.output.andrew_repository import AndrewRepository
from titanic_m_learning.adapter.inbound.api.schemas.andrew_query_schema import AndrewIntroduceResponse, AndrewIntroduceSchema
from titanic_m_learning.app.dtos.andrew_dto import AndrewIntroduceQuery


class AndrewQueryInteractor(AndrewUseCase):
    def __init__(self, repository: AndrewRepository) -> None:
        self._repository = repository

    async def find_page(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> AndrewPageQueryResult:
        return await self._repository.find_page(skip=skip, limit=limit)
    async def introduce_myself(self, schema: AndrewIntroduceSchema) -> AndrewIntroduceResponse:
        result = await self._repository.introduce_myself(
            AndrewIntroduceQuery(id=schema.id, name=schema.name)
        )
        return AndrewIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

