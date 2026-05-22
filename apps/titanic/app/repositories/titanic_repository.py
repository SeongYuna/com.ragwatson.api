"""walter_reader.py → CSV 데이터 접근 레이어."""

from pathlib import Path

import pandas as pd

from titanic.app.models.titanic_passenger import TARGET_COLUMN
from titanic.app.validators.titanic_validator import TitanicValidator

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = _DATA_DIR / "titanic_dataset.csv"


class TitanicRepository:
    def __init__(self) -> None:
        self.csv_path = CSV_PATH
        self._validator = TitanicValidator()

    def load_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.csv_path)
        self._validator.validate_dataframe(df)
        return df

    def get_sample_row(self) -> pd.DataFrame:
        df = self.load_dataframe()
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    def get_count(self) -> int:
        return len(self.load_dataframe())

    def get_survived_count(self) -> int:
        df = self.load_dataframe()
        return int(df[TARGET_COLUMN].fillna(0).astype(int).sum())

    def get_dead_count(self) -> int:
        df = self.load_dataframe()
        return int((df[TARGET_COLUMN].fillna(0).astype(int) == 0).sum())
