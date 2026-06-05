from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.walter_dto import WalterPassengerQuery


class WalterRepository(ABC):
    @abstractmethod
    async def find_all(self) -> list[WalterPassengerQuery]:
        """저장소에서 PersonQuery + BookingQuery 목록을 조회한다."""
        ...
