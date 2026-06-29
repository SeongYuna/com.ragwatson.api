from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.caledon_dto import CaledonStatsResult
from titanic_machine_learning.app.dtos.caledon_dto import CaledonIntroduceQuery, CaledonIntroduceResult


class CaledonPort(ABC):
    @abstractmethod
    async def fetch_stats(self) -> CaledonStatsResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: CaledonIntroduceQuery) -> CaledonIntroduceResult:
        ...

