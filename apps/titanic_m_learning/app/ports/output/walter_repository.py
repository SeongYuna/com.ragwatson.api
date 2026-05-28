from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class WalterRepository(ABC):
    @abstractmethod
    async def find_all(self) -> list[TitanicPassenger]:
        """저장소에서 전체 탑승객 목록을 조회한다."""
        ...
