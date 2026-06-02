from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class IsadorUseCase(ABC):
    @abstractmethod
    async def find_families(self) -> list[TitanicPassenger]:
        """동반 가족·커플 등 연관 승객 목록을 조회한다."""
        ...
