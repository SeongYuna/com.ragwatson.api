from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.stats_result import StatsResult


class CaledonUseCase(ABC):
    @abstractmethod
    async def calculate_stats(self) -> StatsResult:
        """생존률 등 탑승객 통계를 계산한다."""
        ...
