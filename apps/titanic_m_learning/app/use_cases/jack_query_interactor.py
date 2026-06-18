import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import GradientBoostingClassifier, HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult, JackPassengerQuery, JackTrainBundle
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.output.jack_repository import JackRepository


def _preprocess(rows) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """JackTrainRow 리스트 → (X_raw, X_std, y) 반환."""
    df = pd.DataFrame([
        {
            "survived": r.survived, "pclass": r.pclass, "sex": r.sex,
            "age": r.age, "sib_sp": r.sib_sp, "parch": r.parch,
            "fare": r.fare, "embarked": r.embarked,
        }
        for r in rows
    ])

    for col in ["survived", "pclass", "age", "sib_sp", "parch", "fare"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["sex"] = df["sex"].map({"male": 0, "female": 1})
    df["embarked"] = df["embarked"].map({"S": 0, "C": 1, "Q": 2}).fillna(0)
    df["age"] = df["age"].fillna(df["age"].median())
    df["fare"] = df["fare"].fillna(df["fare"].median())
    df = df.dropna()

    # 피처 엔지니어링
    df["family_size"] = df["sib_sp"] + df["parch"]
    df["is_alone"] = (df["family_size"] == 0).astype(int)
    df["age_bin"] = pd.cut(df["age"], bins=[0, 12, 18, 35, 60, 120], labels=[0, 1, 2, 3, 4]).astype(float)

    features = ["pclass", "sex", "age", "fare", "sib_sp", "parch", "embarked", "family_size", "is_alone", "age_bin"]
    X = df[features].values
    y = df["survived"].values.astype(int)
    X_std = StandardScaler().fit_transform(X)
    return X, X_std, y


class JackQueryInteractor(JackUseCase):
    def __init__(self, repository: JackRepository) -> None:
        self._repository = repository

    async def train_model(self) -> JackTrainBundle:
        """로즈가 제안한 모델들을 훈련시키는 메소드."""
        rows = await self._repository.fetch_all_for_training()
        X, X_std, y = _preprocess(rows)

        # 80/20 분할 — 테스트셋은 Caledon에게 전달
        X_train, X_test, X_std_train, X_std_test, y_train, y_test = train_test_split(
            X, X_std, y, test_size=0.2, random_state=42, stratify=y
        )

        # PCA 훈련 데이터로만 fit
        pca = PCA(n_components=5, random_state=42)
        X_pca_train = pca.fit_transform(X_std_train)
        X_pca_test = pca.transform(X_std_test)

        # 1. XGBoost 대체 — GradientBoostingClassifier
        xgb = GradientBoostingClassifier(n_estimators=200, learning_rate=0.05, max_depth=4, random_state=42)
        xgb.fit(X_train, y_train)

        # 2. Random Forest — 배깅 앙상블
        rf = RandomForestClassifier(n_estimators=200, max_depth=6, random_state=42)
        rf.fit(X_train, y_train)

        # 3. LightGBM 대체 — HistGradientBoostingClassifier (리프 중심 유사)
        lgbm = HistGradientBoostingClassifier(max_iter=200, learning_rate=0.05, max_depth=4, random_state=42)
        lgbm.fit(X_train, y_train)

        # 4. CatBoost 대체 — HistGradientBoostingClassifier (범주형 자동 처리)
        catboost = HistGradientBoostingClassifier(max_iter=200, random_state=42)
        catboost.fit(X_train, y_train)

        # 5. Logistic Regression — 표준화 피처 사용
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_std_train, y_train)

        # 6. Decision Tree — 규칙 기반
        dt = DecisionTreeClassifier(max_depth=5, random_state=42)
        dt.fit(X_train, y_train)

        # 7. SVM — 표준화 필수
        svm = SVC(kernel="rbf", C=1.0, probability=True, random_state=42)
        svm.fit(X_std_train, y_train)

        # 8. KNN — 표준화 필수
        knn = KNeighborsClassifier(n_neighbors=5)
        knn.fit(X_std_train, y_train)

        # 9. Naive Bayes
        nb = GaussianNB()
        nb.fit(X_std_train, y_train)

        # 10. KMeans+PCA — PCA 변환 피처로 LR 훈련
        lr_pca = LogisticRegression(max_iter=1000, random_state=42)
        lr_pca.fit(X_pca_train, y_train)

        return JackTrainBundle(
            trained_models={
                "XGBoost(GBM)":        ("raw",  xgb),
                "RandomForest":        ("raw",  rf),
                "LightGBM(HistGBM)":   ("raw",  lgbm),
                "CatBoost(HistGBM)":   ("raw",  catboost),
                "LogisticRegression":  ("std",  lr),
                "DecisionTree":        ("raw",  dt),
                "SVM":                 ("std",  svm),
                "KNN":                 ("std",  knn),
                "NaiveBayes":          ("std",  nb),
                "KMeans+PCA+LR":       ("pca",  lr_pca),
            },
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
