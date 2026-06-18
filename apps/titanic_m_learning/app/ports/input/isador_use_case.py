from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery, IsadorIntroduceQuery, IsadorIntroduceResult


class IsadorUseCase(ABC):
    @abstractmethod
    async def find_families(self) -> list[IsadorPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        ...
