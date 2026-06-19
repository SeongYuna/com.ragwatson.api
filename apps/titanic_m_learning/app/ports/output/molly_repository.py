from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult


class MollyRepository(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        ...
