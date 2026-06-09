from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatQueryResult
from titanic_m_learning.app.dtos.lowe_dto import LoweIntroduceQuery, LoweIntroduceResult


class LoweRepository(ABC):
    @abstractmethod
    async def find_lifeboats(self, *, lifeboat: str | None = None) -> LoweLifeboatQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: LoweIntroduceQuery) -> LoweIntroduceResult:
        ...

