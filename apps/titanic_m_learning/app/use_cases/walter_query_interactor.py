from titanic_m_learning.app.dtos.table_query_result import TableQueryResult
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository


class WalterQueryInteractor(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def find_all(self) -> TableQueryResult:
        queries = await self._repository.find_all()
        return TableQueryResult(passengers=queries)
