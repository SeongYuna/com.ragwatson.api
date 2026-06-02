from titanic_m_learning.app.dtos.stats_result import StatsResult
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase


class CaledonQuery(CaledonUseCase):
    async def calculate_stats(self) -> StatsResult:
        raise NotImplementedError("Cal 생존률 계산은 아직 구현되지 않았습니다.")
