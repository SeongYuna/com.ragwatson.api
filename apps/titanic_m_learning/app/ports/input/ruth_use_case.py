from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.ruth_dto import RuthPassengerQuery
from titanic_m_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthIntroduceResponse, RuthIntroduceSchema


class RuthUseCase(ABC):
    @abstractmethod
    async def find_first_class(self) -> list[RuthPassengerQuery]:
        """1등석 승객 목록을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: RuthIntroduceSchema) -> RuthIntroduceResponse:
        """Ruth 자기소개."""
        ...

