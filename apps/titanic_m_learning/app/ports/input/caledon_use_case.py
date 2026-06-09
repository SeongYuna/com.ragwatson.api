from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.caledon_dto import CaledonStatsResult
from titanic_m_learning.adapter.inbound.api.schemas.cal_query_schema import CaledonIntroduceResponse, CaledonIntroduceSchema


class CaledonUseCase(ABC):
    @abstractmethod
    async def calculate_stats(self) -> CaledonStatsResult:
        """생존률 등 탑승객 통계를 계산한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: CaledonIntroduceSchema) -> CaledonIntroduceResponse:
        """Caledon 자기소개."""
        ...

