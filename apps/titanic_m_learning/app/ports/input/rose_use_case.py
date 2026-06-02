from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.dataset_info_result import DatasetInfoResult


class RoseUseCase(ABC):
    @abstractmethod
    async def get_dataset_info(self) -> DatasetInfoResult:
        """데이터셋 컬럼 설명 등 메타 정보를 반환한다."""
        ...
