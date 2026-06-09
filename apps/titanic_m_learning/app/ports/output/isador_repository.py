from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery
from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult


class IsadorRepository(ABC):
    @abstractmethod
    async def find_families(self) -> list[IsadorPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        ...

