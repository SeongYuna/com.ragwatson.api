from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult
from titanic_m_learning.app.dtos.smith_dto import SmithIntroduceQuery, SmithIntroduceResult
from titanic_m_learning.app.dtos.smith_dto import SmithChatQuery, SmithChatResult

class SmithPort(ABC):
    @abstractmethod
    async def fetch_summary(self) -> SmithStatsResult:
        ...

    @abstractmethod
    async def introduce_myself(self, query: SmithIntroduceQuery) -> SmithIntroduceResult:
        ...

    @abstractmethod
    async def generate_reply(self, query: SmithChatQuery) -> SmithChatResult:
        """Smith 페르소나로 대화 응답을 생성한다."""
        ...
