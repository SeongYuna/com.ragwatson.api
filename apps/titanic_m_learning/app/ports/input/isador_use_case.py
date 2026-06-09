from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery
from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorIntroduceResponse, IsadorIntroduceSchema


class IsadorUseCase(ABC):
    @abstractmethod
    async def find_families(self) -> list[IsadorPassengerQuery]:
        """가족 동반 승객 목록을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: IsadorIntroduceSchema) -> IsadorIntroduceResponse:
        """Isador 자기소개."""
        ...

