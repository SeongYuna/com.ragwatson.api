from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.ports.output.isador_port import IsadorPort
from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult


class IsadorQueryInteractor(IsadorUseCase):
    def __init__(self, repository: IsadorPort) -> None:
        self._repository = repository

    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        return await self._repository.introduce_myself(query)
