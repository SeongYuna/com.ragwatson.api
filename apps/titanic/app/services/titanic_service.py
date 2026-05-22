"""jack_service.py + rose 학습 로직 → 비즈니스 레이어."""

import logging
from pathlib import Path

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

from titanic.app.models.titanic_passenger import (
    COLUMN_SPECS,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)
from titanic.app.repositories.titanic_model_repository import TitanicModelRepository
from titanic.app.repositories.titanic_repository import TitanicRepository
from titanic.app.schemas.titanic_schema import TitanicColumnDocSchema, TitanicDatasetInfoSchema

logger = logging.getLogger(__name__)


class TitanicService:
    def __init__(self) -> None:
        self.repository = TitanicRepository()
        self.model_repository = TitanicModelRepository()

    def get_data(self) -> pd.DataFrame:
        return self.repository.get_sample_row()

    def get_count(self) -> int:
        return self.repository.get_count()

    def get_survived_count(self) -> int:
        return self.repository.get_survived_count()

    def get_dead_count(self) -> int:
        return self.repository.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self.model_repository.has_model()

    def get_current_model_name(self) -> str | None:
        return self.model_repository.get_model_name()

    def get_dataset_info(self) -> TitanicDatasetInfoSchema:
        return TitanicDatasetInfoSchema(
            columns=[
                TitanicColumnDocSchema(
                    name=spec.name,
                    description=spec.description,
                    role=spec.role,
                )
                for spec in COLUMN_SPECS
            ],
        )

    def _prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        work = df[FEATURE_COLUMNS + [TARGET_COLUMN]].copy()
        work["Sex"] = work["Sex"].map({"male": 0, "female": 1})
        work["Age"] = work["Age"].fillna(work["Age"].median())
        work["Fare"] = work["Fare"].fillna(work["Fare"].median())
        work = work.dropna(subset=[TARGET_COLUMN])
        return work

    def train_and_save_model(self) -> Path:
        df = self.repository.load_dataframe()
        prepared = self._prepare_features(df)
        x = prepared[FEATURE_COLUMNS]
        y = prepared[TARGET_COLUMN].astype(int)

        model = DecisionTreeClassifier(random_state=42)
        model.fit(x, y)

        path = self.model_repository.save_model(model)
        logger.info("[TitanicService] decision tree 학습 완료 — path=%s", path)
        return path
