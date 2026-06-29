from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.andrew_dto import AndrewPageQueryResult
from titanic_machine_learning.app.dtos.andrew_dto import AndrewIntroduceQuery, AndrewIntroduceResult


class AndrewPort(ABC):
    @abstractmethod
    async def find_page(self, *, skip: int, limit: int) -> AndrewPageQueryResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: AndrewIntroduceQuery) -> AndrewIntroduceResult:
        ...

