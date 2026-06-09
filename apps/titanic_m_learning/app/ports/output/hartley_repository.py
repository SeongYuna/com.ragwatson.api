from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.hartley_dto import HartleyPassengerQuery
from titanic_m_learning.app.dtos.hartley_dto import HartleyIntroduceQuery, HartleyIntroduceResult


class HartleyRepository(ABC):
    @abstractmethod
    async def sample(self, *, count: int) -> list[HartleyPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: HartleyIntroduceQuery) -> HartleyIntroduceResult:
        ...

