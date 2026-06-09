from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.hartley_dto import HartleyPassengerQuery
from titanic_m_learning.adapter.inbound.api.schemas.hartley_query_schema import HartleyIntroduceResponse, HartleyIntroduceSchema


class HartleyUseCase(ABC):
    @abstractmethod
    async def sample(self, *, count: int = 10) -> list[HartleyPassengerQuery]:
        """무작위 승객 샘플을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: HartleyIntroduceSchema) -> HartleyIntroduceResponse:
        """Hartley 자기소개."""
        ...

