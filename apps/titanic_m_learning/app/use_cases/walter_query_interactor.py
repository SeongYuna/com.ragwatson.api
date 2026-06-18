from titanic_m_learning.app.dtos.walter_dto import (
    WalterTableQueryResult,
    WalterPassengerQuery,
    WalterIntroduceQuery,
    WalterIntroduceResult,
)
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository


class WalterQueryInteractor(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def find_all(self) -> WalterTableQueryResult:
        queries = await self._repository.find_all()
        return WalterTableQueryResult(passengers=queries)

    async def introduce_myself(self, query: WalterIntroduceQuery) -> WalterIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def get_train_set(self) -> list[WalterPassengerQuery]:
        return await self._repository.get_train_set()

    async def get_test_set(self) -> list[WalterPassengerQuery]:
        return await self._repository.get_test_set()
