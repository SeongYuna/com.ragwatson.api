from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class JamesRepository(ABC):
    @abstractmethod
    async def save_all(self, passengers: list[TitanicPassenger]) -> None:
        """도메인 탑승객 목록을 저장소에 저장한다."""
        ...
