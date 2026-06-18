from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.smith_dto import (
    SmithStatsResult,
    SmithIntroduceQuery,
    SmithIntroduceResult,
    SmithChatQuery,
    SmithChatResult,
)


class SmithUseCase(ABC):
    @abstractmethod
    async def get_summary(self) -> SmithStatsResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: SmithIntroduceQuery) -> SmithIntroduceResult:
        ...

    @abstractmethod
    async def chat(self, query: SmithChatQuery) -> SmithChatResult:
        ...
