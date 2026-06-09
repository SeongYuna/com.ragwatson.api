from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatQueryResult
from titanic_m_learning.adapter.inbound.api.schemas.lowe_query_schema import LoweIntroduceResponse, LoweIntroduceSchema


class LoweUseCase(ABC):
    @abstractmethod
    async def find_lifeboats(
        self,
        *,
        lifeboat: str | None = None,
    ) -> LoweLifeboatQueryResult:
        """구명보트 탑승 승객 Query DTO 목록을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: LoweIntroduceSchema) -> LoweIntroduceResponse:
        """Lowe 자기소개."""
        ...

