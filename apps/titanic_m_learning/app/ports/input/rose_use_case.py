from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.rose_dto import (
    RoseDatasetInfoResult,
    RosePredictQuery,
    RosePredictResult,
    RoseIntroduceQuery,
    RoseIntroduceResult,
)


class MLAlgorithmStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        ...


class RoseUseCase(ABC):
    @abstractmethod
    async def get_dataset_info(self) -> RoseDatasetInfoResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: RoseIntroduceQuery) -> RoseIntroduceResult:
        ...

    @abstractmethod
    async def predict(self, query: RosePredictQuery, strategy: MLAlgorithmStrategy) -> RosePredictResult:
        ...

    @abstractmethod
    async def predict_by_algorithm(self, query: RosePredictQuery, algorithm: str) -> RosePredictResult:
        ...
