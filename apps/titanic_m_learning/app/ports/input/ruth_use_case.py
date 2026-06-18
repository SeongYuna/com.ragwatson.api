from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.ruth_dto import RuthPassengerQuery, RuthIntroduceQuery, RuthIntroduceResult


class RuthUseCase(ABC):
    @abstractmethod
    async def find_first_class(self) -> list[RuthPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        ...
