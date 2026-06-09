from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.caledon_dto import CaledonStatsResult
from titanic_m_learning.app.dtos.caledon_dto import CaledonIntroduceQuery, CaledonIntroduceResult


class CaledonRepository(ABC):
    @abstractmethod
    async def fetch_stats(self) -> CaledonStatsResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: CaledonIntroduceQuery) -> CaledonIntroduceResult:
        ...

