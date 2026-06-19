import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult, JackPassengerQuery, JackTrainBundle
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.output.jack_repository import JackRepository


class JackQueryInteractor(JackUseCase):
    def __init__(self, repository: JackRepository, lowe: LoweUseCase, rose: RoseUseCase) -> None:
        self._repository = repository
        self._lowe = lowe
        self._rose = rose

    async def train_model(self) -> JackTrainBundle:
        """전처리는 Lowe, 모델 제안은 Rose에 위임하고 Jack은 훈련(fit)만 담당한다."""
        rows = await self._repository.fetch_all_for_training()

        # 원시 행 → DataFrame (컬럼명은 Lowe.feature_engineering 입력 스키마와 일치)
        train_df = pd.DataFrame([
            {
                "passenger_id": r.passenger_id, "name": r.name, "gender": r.gender,
                "survived": r.survived, "pclass": r.pclass, "age": r.age,
                "sib_sp": r.sib_sp, "parch": r.parch, "ticket": r.ticket,
                "fare": r.fare, "cabin": r.cabin, "embarked": r.embarked,
            }
            for r in rows
        ])

        # 피처 엔지니어링은 Lowe가 담당. 잔여 컬럼을 수치화해 모델 입력으로 정리.
        feat_df = self._lowe.feature_engineering(train_df)
        feat_df = feat_df.apply(pd.to_numeric, errors="coerce").fillna(0)
        y = feat_df["survived"].astype(int).values
        X = feat_df.drop(columns=["survived"]).values.astype(float)
        X_std = StandardScaler().fit_transform(X)

        # 80/20 분할 — 테스트셋은 Caledon에게 전달
        X_train, X_test, X_std_train, X_std_test, y_train, y_test = train_test_split(
            X, X_std, y, test_size=0.2, random_state=42, stratify=y
        )

        # PCA 훈련 데이터로만 fit
        pca = PCA(n_components=5, random_state=42)
        X_pca_train = pca.fit_transform(X_std_train)
        X_pca_test = pca.transform(X_std_test)

        # 입력 타입별 훈련 피처
        train_features = {"raw": X_train, "std": X_std_train, "pca": X_pca_train}

        # Rose가 제안한 미훈련 estimator를 받아 Jack이 fit만 수행한다.
        trained_models: dict[str, tuple[str, object]] = {}
        for name, (input_type, estimator) in self._rose.propose_models().items():
            estimator.fit(train_features[input_type], y_train)
            trained_models[name] = (input_type, estimator)

        return JackTrainBundle(
            trained_models=trained_models,
            X_test=X_std_test,
            X_test_raw=X_test,
            X_test_pca=X_pca_test,
            y_test=y_test,
        )

    async def analyze_message_incent(self, user_message: str) -> list:
        return []

    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        return await self._repository.find_by_id(passenger_id)

    async def introduce_myself(self, query: JackIntroduceQuery) -> JackIntroduceResult:
        return await self._repository.introduce_myself(query)
