from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.jack_dto import JackPassengerQuery
from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult


class JackRepository(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        ...

    @abstractmethod
    async def introduce_myself(self, query: JackIntroduceQuery) -> JackIntroduceResult:
        ...

