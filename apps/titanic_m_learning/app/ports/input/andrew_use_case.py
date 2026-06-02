from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class AndrewUseCase(ABC):
    @abstractmethod
    async def find_page(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TitanicPassenger]:
        """탑승객 목록을 페이지 단위로 조회한다."""
        ...
