from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.caledon_dto import CaledonModelTestResult, CaledonStatsResult, CaledonIntroduceQuery, CaledonIntroduceResult
from titanic_machine_learning.app.dtos.jack_dto import JackTrainBundle


class CaledonUseCase(ABC):
    @abstractmethod
    async def calculate_stats(self) -> CaledonStatsResult:
        """생존률 등 탑승객 통계를 계산한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, query: CaledonIntroduceQuery) -> CaledonIntroduceResult:
        """Caledon 자기소개."""
        ...

    @abstractmethod
    async def test_model(self, bundle: JackTrainBundle) -> CaledonModelTestResult:
        """잭이 훈련한 모델들을 테스트 셋으로 평가하고 점수화해서 1등을 반환한다."""
        ...
