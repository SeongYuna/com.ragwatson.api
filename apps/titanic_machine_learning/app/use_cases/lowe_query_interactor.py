from __future__ import annotations

import numpy as np
import pandas as pd

from titanic_machine_learning.app.dtos.lowe_dto import (
    LoweLifeboatQueryResult,
    LoweIntroduceQuery,
    LoweIntroduceResult,
)
from titanic_machine_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_machine_learning.app.ports.output.lowe_port import LowePort


class LoweQueryInteractor(LoweUseCase):
    def __init__(self, repository: LowePort) -> None:
        self._repository = repository

    async def find_lifeboats(self, *, lifeboat: str | None = None) -> LoweLifeboatQueryResult:
        return await self._repository.find_lifeboats(lifeboat=lifeboat)

    async def introduce_myself(self, query: LoweIntroduceQuery) -> LoweIntroduceResult:
        return await self._repository.introduce_myself(query)

    def feature_engineering(self, train_set) -> pd.DataFrame:
        """피처 엔지니어링 — Title·AgeGroup·FareBand 파생 + 불필요 컬럼 드롭."""
        train = train_set.copy()

        # 1. 호칭 추출 및 Nominal 변환
        train["Title"] = train["name"].str.extract(r"([A-Za-z]+)\.", expand=False)
        train["Title"] = train["Title"].replace(
            ["Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme"], "Rare"
        )
        train["Title"] = train["Title"].replace(["Countess", "Lady", "Sir"], "Royal")
        train["Title"] = train["Title"].replace({"Mlle": "Mr", "Ms": "Miss"})
        title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6}
        train["Title"] = train["Title"].map(title_mapping).fillna(0).astype(int)

        # 2. 성별 Nominal 변환 (female=1, male=0)
        train["gender"] = train["gender"].map({"male": 0, "female": 1})

        # 3. 나이 구간 Ordinal 변환
        age_title_mapping = {
            0: "Unknown", 1: "Baby", 2: "Child", 3: "Teenager",
            4: "Student", 5: "Young Adult", 6: "Adult", 7: "Senior",
        }
        age_mapping = {v: k for k, v in age_title_mapping.items()}
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        age_labels = list(age_title_mapping.values())

        train["age"] = pd.to_numeric(train["age"], errors="coerce").fillna(-0.5)
        train["AgeGroup"] = pd.cut(train["age"], bins, labels=age_labels).astype(str)
        mask = train["AgeGroup"] == "Unknown"
        train.loc[mask, "AgeGroup"] = train.loc[mask, "Title"].map(age_title_mapping)
        train["AgeGroup"] = train["AgeGroup"].map(age_mapping).fillna(0).astype(int)

        # 4. 승선항 Nominal 변환
        train["embarked"] = train["embarked"].fillna("S").map({"S": 1, "C": 2, "Q": 3})

        # 5. 요금 Ordinal 변환
        train["fare"] = pd.to_numeric(train["fare"], errors="coerce").fillna(0)
        train["FareBand"] = (
            pd.qcut(train["fare"], 4, labels=[1, 2, 3, 4], duplicates="drop")
            .fillna(1).astype(int)
        )

        drop_cols = ["name", "age", "fare", "ticket", "cabin", "passenger_id"]
        return train.drop(columns=[c for c in drop_cols if c in train.columns])
