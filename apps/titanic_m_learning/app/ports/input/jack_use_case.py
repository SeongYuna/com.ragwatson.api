from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.jack_dto import JackPassengerQuery
from titanic_m_learning.adapter.inbound.api.schemas.jack_query_schema import JackIntroduceResponse, JackIntroduceSchema


class JackUseCase(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        """passenger_id로 승객 1명을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: JackIntroduceSchema) -> JackIntroduceResponse:
        """Jack 자기소개."""
        ...

