from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult
from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult


class MollyRepository(ABC):
    @abstractmethod
    async def find_notable(self) -> MollyNotableQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        ...

