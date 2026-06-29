from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult


class IsadorUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        ...
