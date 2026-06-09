from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.walter_dto import WalterTableQueryResult
from titanic_m_learning.adapter.inbound.api.schemas.walter_query_schema import WalterIntroduceResponse, WalterIntroduceSchema


class WalterUseCase(ABC):
    @abstractmethod
    async def find_all(self) -> WalterTableQueryResult:
        """전체 탑승객 목록을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: WalterIntroduceSchema) -> WalterIntroduceResponse:
        """Walter 자기소개."""
        ...

