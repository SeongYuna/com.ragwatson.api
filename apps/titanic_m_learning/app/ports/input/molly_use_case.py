from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult, MollyIntroduceQuery, MollyIntroduceResult


class MollyUseCase(ABC):
    @abstractmethod
    async def find_notable(self) -> MollyNotableQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        ...
