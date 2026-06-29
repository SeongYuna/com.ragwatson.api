from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.walter_dto import WalterTableQueryResult, WalterPassengerQuery, WalterIntroduceQuery, WalterIntroduceResult


class WalterUseCase(ABC):
    @abstractmethod
    async def find_all(self) -> WalterTableQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: WalterIntroduceQuery) -> WalterIntroduceResult:
        ...

    @abstractmethod
    async def get_train_set(self) -> list[WalterPassengerQuery]:
        ...

    @abstractmethod
    async def get_test_set(self) -> list[WalterPassengerQuery]:
        ...
