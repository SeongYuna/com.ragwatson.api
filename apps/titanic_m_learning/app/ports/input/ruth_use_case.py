from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class RuthUseCase(ABC):
    @abstractmethod
    async def find_first_class(self) -> list[TitanicPassenger]:
        """1등석 탑승객 목록을 조회한다."""
        ...
