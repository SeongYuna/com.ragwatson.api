from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.stats_result import StatsResult


class SmithUseCase(ABC):
    @abstractmethod
    async def get_summary(self) -> StatsResult:
        """전체 탑승객 요약 통계를 반환한다."""
        ...
