from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.ruth_dto import RuthPassengerQuery
from titanic_m_learning.app.dtos.ruth_dto import RuthIntroduceQuery, RuthIntroduceResult


class RuthRepository(ABC):
    @abstractmethod
    async def find_first_class(self) -> list[RuthPassengerQuery]:
        ...

    @abstractmethod
    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        ...

