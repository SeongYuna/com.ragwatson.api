from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.ruth_dto import RuthIntroduceQuery, RuthIntroduceResult


class RuthPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        ...
