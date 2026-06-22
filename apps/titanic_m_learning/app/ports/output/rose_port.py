from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.rose_dto import RoseDatasetInfoResult
from titanic_m_learning.app.dtos.rose_dto import RoseIntroduceQuery, RoseIntroduceResult


class RosePort(ABC):
    @abstractmethod
    async def fetch_dataset_info(self) -> RoseDatasetInfoResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: RoseIntroduceQuery) -> RoseIntroduceResult:
        ...

