from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.rose_dto import RoseDatasetInfoResult
from titanic_m_learning.adapter.inbound.api.schemas.rose_query_schema import RoseIntroduceResponse, RoseIntroduceSchema


class RoseUseCase(ABC):
    @abstractmethod
    async def get_dataset_info(self) -> RoseDatasetInfoResult:
        """타이타닉 데이터셋 컬럼 메타정보를 반환한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: RoseIntroduceSchema) -> RoseIntroduceResponse:
        """Rose 자기소개."""
        ...

