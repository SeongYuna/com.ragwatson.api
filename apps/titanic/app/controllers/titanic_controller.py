"""james_controller.py → API 진입 레이어 (James → TitanicController)."""

import logging
from pathlib import Path

import pandas as pd

from titanic.app.schemas.titanic_schema import TitanicDatasetInfoSchema
from titanic.app.services.titanic_service import TitanicService

logger = logging.getLogger(__name__)


class TitanicController:
    def __init__(self) -> None:
        self.titanic_service = TitanicService()

    def get_data(self) -> pd.DataFrame:
        return self.titanic_service.get_data()

    def get_count(self) -> int:
        return self.titanic_service.get_count()

    def get_survived_count(self) -> int:
        return self.titanic_service.get_survived_count()

    def get_dead_count(self) -> int:
        return self.titanic_service.get_dead_count()

    def has_decision_tree_model(self) -> bool:
        return self.titanic_service.has_decision_tree_model()

    def train_decision_tree_model(self) -> Path:
        path = self.titanic_service.train_and_save_model()
        logger.info("[TitanicController] train_decision_tree_model 완료")
        return path

    def get_current_model_name(self) -> str | None:
        return self.titanic_service.get_current_model_name()

    def get_dataset_info(self) -> TitanicDatasetInfoSchema:
        return self.titanic_service.get_dataset_info()
