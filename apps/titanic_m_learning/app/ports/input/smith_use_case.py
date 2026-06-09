from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult
from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import SmithIntroduceResponse, SmithIntroduceSchema


class SmithUseCase(ABC):
    @abstractmethod
    async def get_summary(self) -> SmithStatsResult:
        """전체 탑승객 요약 통계를 반환한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: SmithIntroduceSchema) -> SmithIntroduceResponse:
        """Smith 자기소개."""
        ...

