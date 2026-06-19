from typing import Any

from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from titanic_m_learning.app.dtos.rose_dto import (
    RoseDatasetInfoResult,
    RoseIntroduceQuery,
    RoseIntroduceResult,
    RosePredictQuery,
    RosePredictResult,
)
from titanic_m_learning.app.ports.input.rose_use_case import MLAlgorithmStrategy, RoseUseCase
from titanic_m_learning.app.ports.output.rose_repository import RoseRepository


# ──────────────────────────────────────────────
# 전략 구현체 10개
# ──────────────────────────────────────────────

class XGBoostStrategy(MLAlgorithmStrategy):
    """그래디언트 부스팅 기반 고성능 모델. 과적합 방지 규제 내장."""

    @property
    def name(self) -> str:
        return "XGBoost"

    def build_estimator(self) -> tuple[str, Any]:
        return "raw", GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        score = 0.0
        score += 0.4 if query.sex == "female" else 0.0
        score += 0.2 if query.pclass == 1 else (0.1 if query.pclass == 2 else 0.0)
        score += 0.15 if query.age < 16 else 0.0
        score += 0.1 if (query.sibsp + query.parch) in range(1, 4) else 0.0
        score += 0.05 if query.fare > 50 else 0.0
        probability = min(score, 0.99)
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class RandomForestStrategy(MLAlgorithmStrategy):
    """다수의 결정 트리를 배깅하는 앙상블 모델. 노이즈에 강건."""

    @property
    def name(self) -> str:
        return "RandomForest"

    def build_estimator(self) -> tuple[str, Any]:
        return "raw", RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        votes = [
            query.sex == "female",
            query.pclass <= 2,
            query.age < 18 or query.age > 60,
            query.fare > 30,
            (query.sibsp + query.parch) < 5,
        ]
        probability = sum(votes) / len(votes)
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class LightGBMStrategy(MLAlgorithmStrategy):
    """리프 중심 트리 분할. 대용량 처리 특화, 빠른 속도."""

    @property
    def name(self) -> str:
        return "LightGBM"

    def build_estimator(self) -> tuple[str, Any]:
        return "raw", HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_depth=4, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        score = 0.0
        score += 0.45 if query.sex == "female" else 0.0
        score += 0.25 if query.pclass == 1 else (0.1 if query.pclass == 2 else 0.0)
        score += 0.1 if query.age < 15 else 0.0
        score += 0.1 if query.fare > 100 else (0.05 if query.fare > 30 else 0.0)
        score += 0.05 if 1 <= (query.sibsp + query.parch) <= 3 else 0.0
        probability = min(score, 0.99)
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class CatBoostStrategy(MLAlgorithmStrategy):
    """범주형 피처 자동 처리 부스팅. 별도 인코딩 불필요."""

    @property
    def name(self) -> str:
        return "CatBoost"

    def build_estimator(self) -> tuple[str, Any]:
        return "raw", HistGradientBoostingClassifier(max_iter=200, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # 범주형(sex, pclass) 피처 중심 점수 계산
        sex_score = 0.5 if query.sex == "female" else 0.1
        class_score = {1: 0.35, 2: 0.2, 3: 0.05}.get(query.pclass, 0.05)
        age_score = 0.1 if query.age < 16 else 0.0
        probability = min(sex_score + class_score + age_score, 0.99)
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class LogisticRegressionStrategy(MLAlgorithmStrategy):
    """선형 관계 기반 이진 분류. 피처 영향력 해석에 유리."""

    @property
    def name(self) -> str:
        return "LogisticRegression"

    def build_estimator(self) -> tuple[str, Any]:
        return "std", LogisticRegression(max_iter=1000, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        import math
        # 로지스틱 회귀 근사: logit = w0 + w1*sex + w2*pclass + w3*age
        sex_val = 1.0 if query.sex == "female" else 0.0
        logit = -1.2 + (2.5 * sex_val) + (-0.8 * query.pclass) + (-0.02 * query.age) + (0.002 * query.fare)
        probability = 1 / (1 + math.exp(-logit))
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class DecisionTreeStrategy(MLAlgorithmStrategy):
    """나무 가지치기 형태의 규칙 기반 모델. 결과 시각화 용이."""

    @property
    def name(self) -> str:
        return "DecisionTree"

    def build_estimator(self) -> tuple[str, Any]:
        return "raw", DecisionTreeClassifier(max_depth=5, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # 규칙 트리: sex → pclass → age 순 분기
        if query.sex == "female":
            survived = query.pclass in (1, 2) or query.age < 18
        else:
            survived = query.pclass == 1 and query.age < 10
        probability = 0.85 if survived else 0.15
        return RosePredictResult(survived=survived, probability=probability, algorithm=self.name)


class SVMStrategy(MLAlgorithmStrategy):
    """마진 최대화 결정 경계 탐색. 표준화된 데이터에서 비선형 관계 파악."""

    @property
    def name(self) -> str:
        return "SVM"

    def build_estimator(self) -> tuple[str, Any]:
        return "std", SVC(kernel="rbf", C=1.0, probability=True, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # RBF 커널 근사: 표준화된 피처 기반 서포트 벡터 점수
        sex_val = 1.0 if query.sex == "female" else -1.0
        age_norm = (query.age - 30) / 15
        fare_norm = (query.fare - 32) / 50
        score = (sex_val * 0.6) + ((-query.pclass + 2) * 0.25) + (-age_norm * 0.1) + (fare_norm * 0.05)
        probability = min(max((score + 1) / 2, 0.01), 0.99)
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class KNNStrategy(MLAlgorithmStrategy):
    """K개 최근접 이웃 기반 분류. 승객 유사도로 생존 여부 추론."""

    @property
    def name(self) -> str:
        return "KNN"

    def build_estimator(self) -> tuple[str, Any]:
        return "std", KNeighborsClassifier(n_neighbors=5)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # 대표 이웃 그룹과의 유사도 점수 (여성 1등석, 남성 3등석 등)
        female_1st = abs(query.pclass - 1) + (0 if query.sex == "female" else 3) + abs(query.age - 35) / 30
        male_3rd = abs(query.pclass - 3) + (0 if query.sex == "male" else 3) + abs(query.age - 28) / 30
        survived = female_1st < male_3rd
        probability = 0.8 if survived else 0.2
        return RosePredictResult(survived=survived, probability=probability, algorithm=self.name)


class NaiveBayesStrategy(MLAlgorithmStrategy):
    """베이즈 정리 기반 조건부 확률 분류. 빠르고 희소 데이터에 강건."""

    @property
    def name(self) -> str:
        return "NaiveBayes"

    def build_estimator(self) -> tuple[str, Any]:
        return "std", GaussianNB()

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # P(survived | features) ∝ P(sex|survived) * P(pclass|survived) * P(age_bin|survived)
        p_sex = 0.74 if query.sex == "female" else 0.19
        p_class = {1: 0.63, 2: 0.47, 3: 0.24}.get(query.pclass, 0.24)
        p_age = 0.54 if query.age < 16 else 0.38
        probability = min((p_sex * p_class * p_age) / 0.15, 0.99)  # 정규화 근사
        return RosePredictResult(survived=probability >= 0.5, probability=round(probability, 4), algorithm=self.name)


class KMeansPCAStrategy(MLAlgorithmStrategy):
    """비지도 학습 기반 군집화 + 차원 축소. 파생 변수 생성 보조 활용."""

    @property
    def name(self) -> str:
        return "KMeans+PCA"

    def build_estimator(self) -> tuple[str, Any]:
        # PCA 변환은 Jack이 수행하고, Rose는 압축 피처용 분류기를 제안한다.
        return "pca", LogisticRegression(max_iter=1000, random_state=42)

    async def predict(self, query: RosePredictQuery) -> RosePredictResult:
        # PCA 근사: 주요 주성분으로 압축 후 생존 군집 거리 계산
        pc1 = (1 if query.sex == "female" else -1) * 0.6 + (2 - query.pclass) * 0.4
        pc2 = (-query.age / 40) * 0.5 + (query.fare / 100) * 0.5
        # 생존 군집 중심 (pc1=0.8, pc2=0.3)과의 거리
        dist = ((pc1 - 0.8) ** 2 + (pc2 - 0.3) ** 2) ** 0.5
        survived = dist < 0.9
        probability = max(0.01, min(1 - dist / 2, 0.99))
        return RosePredictResult(survived=survived, probability=round(probability, 4), algorithm=self.name)


# ──────────────────────────────────────────────
# 인터랙터
# ──────────────────────────────────────────────

class RoseQueryInteractor(RoseUseCase):
    def __init__(self, repository: RoseRepository) -> None:
        self._repository = repository

    async def get_dataset_info(self) -> RoseDatasetInfoResult:
        return await self._repository.fetch_dataset_info()

    async def introduce_myself(self, query: RoseIntroduceQuery) -> RoseIntroduceResult:
        return await self._repository.introduce_myself(query)

    def propose_models(self) -> dict[str, tuple[str, Any]]:
        """훈련할 10가지 알고리즘을 미훈련 estimator로 제안한다. Jack이 받아 fit한다."""
        return {
            strategy.name: strategy.build_estimator()
            for strategy in _STRATEGY_MAP.values()
        }

    async def predict(
        self, query: RosePredictQuery, strategy: MLAlgorithmStrategy
    ) -> RosePredictResult:
        return await strategy.predict(query)

    async def predict_by_algorithm(
        self, query: RosePredictQuery, algorithm: str
    ) -> RosePredictResult:
        strategy = _STRATEGY_MAP.get(algorithm, RandomForestStrategy())
        return await strategy.predict(query)


_STRATEGY_MAP: dict[str, MLAlgorithmStrategy] = {
    "XGBoost":           XGBoostStrategy(),
    "RandomForest":      RandomForestStrategy(),
    "LightGBM":          LightGBMStrategy(),
    "CatBoost":          CatBoostStrategy(),
    "LogisticRegression": LogisticRegressionStrategy(),
    "DecisionTree":      DecisionTreeStrategy(),
    "SVM":               SVMStrategy(),
    "KNN":               KNNStrategy(),
    "NaiveBayes":        NaiveBayesStrategy(),
    "KMeans+PCA":        KMeansPCAStrategy(),
}
