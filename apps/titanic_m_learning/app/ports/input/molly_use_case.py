from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult
from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyIntroduceResponse, MollyIntroduceSchema


class MollyUseCase(ABC):
    @abstractmethod
    async def find_notable(self) -> MollyNotableQueryResult:
        """주목 승객·생존자 Query DTO 목록을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: MollyIntroduceSchema) -> MollyIntroduceResponse:
        """Molly 자기소개."""
        ...

