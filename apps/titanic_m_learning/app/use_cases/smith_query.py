from titanic_m_learning.app.dtos.stats_result import StatsResult
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase


class SmithQuery(SmithUseCase):
    async def get_summary(self) -> StatsResult:
        raise NotImplementedError("Smith 요약 통계는 아직 구현되지 않았습니다.")
