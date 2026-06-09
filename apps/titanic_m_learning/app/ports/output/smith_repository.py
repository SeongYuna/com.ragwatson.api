from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult
from titanic_m_learning.app.dtos.smith_dto import SmithIntroduceQuery, SmithIntroduceResult


class SmithRepository(ABC):
    @abstractmethod
    async def fetch_summary(self) -> SmithStatsResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: SmithIntroduceQuery) -> SmithIntroduceResult:
        ...

