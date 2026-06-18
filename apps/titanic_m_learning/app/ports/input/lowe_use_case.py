from abc import ABC, abstractmethod

import pandas as pd

from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatQueryResult, LoweIntroduceQuery, LoweIntroduceResult


class LoweUseCase(ABC):
    @abstractmethod
    async def find_lifeboats(self, *, lifeboat: str | None = None) -> LoweLifeboatQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: LoweIntroduceQuery) -> LoweIntroduceResult:
        ...

    @abstractmethod
    def feature_engineering(self, train_set) -> pd.DataFrame:
        ...
