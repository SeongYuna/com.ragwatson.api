from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.walter_dto import WalterPassengerQuery
from titanic_machine_learning.app.dtos.walter_dto import WalterIntroduceQuery, WalterIntroduceResult


class WalterPort(ABC):
    @abstractmethod
    async def find_all(self) -> list[WalterPassengerQuery]:
        """저장소에서 PersonQuery + BookingQuery 목록을 조회한다."""
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

