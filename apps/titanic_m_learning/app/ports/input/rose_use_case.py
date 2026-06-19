from abc import ABC, abstractmethod
from typing import Any

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
    def build_estimator(self) -> tuple[str, Any]:
        """훈련 전 sklearn estimator를 제안한다. (input_type, model) — input_type ∈ {"raw", "std", "pca"}."""
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
    def propose_models(self) -> dict[str, tuple[str, Any]]:
        """훈련할 10가지 알고리즘을 미훈련 estimator로 제안한다. name → (input_type, model)."""
        ...

    @abstractmethod
    async def predict(self, query: RosePredictQuery, strategy: MLAlgorithmStrategy) -> RosePredictResult:
        ...

    @abstractmethod
    async def predict_by_algorithm(self, query: RosePredictQuery, algorithm: str) -> RosePredictResult:
        ...
