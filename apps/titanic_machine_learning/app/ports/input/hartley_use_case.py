from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.hartley_dto import HartleyPassengerQuery, HartleyIntroduceQuery, HartleyIntroduceResult


class HartleyUseCase(ABC):
    @abstractmethod
    async def sample(self, *, count: int = 10) -> list[HartleyPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: HartleyIntroduceQuery) -> HartleyIntroduceResult:
        ...

    @abstractmethod
    async def get_correlation_heatmap(self) -> bytes:
        ...
