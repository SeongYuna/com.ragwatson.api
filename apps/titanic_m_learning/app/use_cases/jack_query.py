import logging

from titanic.app.models.titanic_passenger import COLUMN_SPECS
from titanic.app.repositories.titanic_model_repository import TitanicModelRepository
from titanic.app.schemas.titanic_schema import TitanicColumnDocSchema, TitanicDatasetInfoSchema

logger = logging.getLogger(__name__)


class TitanicService:
    def __init__(self) -> None:
        self.model_repository = TitanicModelRepository()

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
