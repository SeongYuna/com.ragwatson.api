from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from titanic_m_learning.app.dtos.caledon_dto import (
    CaledonIntroduceQuery,
    CaledonIntroduceResult,
    CaledonModelScore,
    CaledonModelTestResult,
    CaledonStatsResult,
)
from titanic_m_learning.app.dtos.jack_dto import JackTrainBundle
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.output.caledon_port import CaledonPort


class CaledonQueryInteractor(CaledonUseCase):
    def __init__(self, repository: CaledonPort) -> None:
        self._repository = repository

    async def calculate_stats(self) -> CaledonStatsResult:
        return await self._repository.fetch_stats()

    async def introduce_myself(self, query: CaledonIntroduceQuery) -> CaledonIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def test_model(self, bundle: JackTrainBundle) -> CaledonModelTestResult:
        """잭이 훈련한 모델들을 테스트 셋으로 평가하고 점수화해서 1등을 반환한다."""
        scores: list[CaledonModelScore] = []

        for algorithm, (input_type, model) in bundle.trained_models.items():
            if input_type == "raw":
                X = bundle.X_test_raw
            elif input_type == "pca":
                X = bundle.X_test_pca
            else:  # "std"
                X = bundle.X_test

            y_pred = model.predict(X)
            scores.append(CaledonModelScore(
                algorithm=algorithm,
                accuracy=round(float(accuracy_score(bundle.y_test, y_pred)), 4),
                precision=round(float(precision_score(bundle.y_test, y_pred, zero_division=0)), 4),
                recall=round(float(recall_score(bundle.y_test, y_pred, zero_division=0)), 4),
                f1=round(float(f1_score(bundle.y_test, y_pred, zero_division=0)), 4),
            ))

        winner = max(scores, key=lambda s: s.accuracy)
        return CaledonModelTestResult(
            scores=tuple(scores),
            winner=winner.algorithm,
            winner_accuracy=winner.accuracy,
        )
