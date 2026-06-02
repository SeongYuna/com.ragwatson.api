from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class JackUseCase(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> TitanicPassenger:
        """승객 ID로 탑승객 한 명을 조회한다."""
        ...
