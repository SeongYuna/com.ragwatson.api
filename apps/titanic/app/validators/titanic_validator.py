"""caleden_validation.py → 검증 레이어 (Caledon → TitanicValidator)."""

import pandas as pd

from titanic.app.models.titanic_passenger import (
    CSV_COLUMNS,
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)


class TitanicValidator:
    def validate_dataframe(self, df: pd.DataFrame) -> None:
        missing = [c for c in CSV_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"CSV 필수 컬럼 누락: {missing}")

        for col in FEATURE_COLUMNS + [TARGET_COLUMN]:
            if col not in df.columns:
                raise ValueError(f"학습 컬럼 누락: {col}")

        survived = df[TARGET_COLUMN].dropna()
        if not survived.isin([0, 1]).all():
            raise ValueError(f"{TARGET_COLUMN}는 0 또는 1이어야 합니다.")

    def validate_upload_filename(self, filename: str | None) -> None:
        if not filename or not filename.lower().endswith(".csv"):
            raise ValueError("CSV 파일만 업로드할 수 있습니다.")
