from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult


class IsadorPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        ...
