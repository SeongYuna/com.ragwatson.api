from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult


class MollyUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        ...
