from abc import ABC, abstractmethod

from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class HartleyUseCase(ABC):
    @abstractmethod
    async def sample(self, *, count: int = 10) -> list[TitanicPassenger]:
        """탑승객 목록에서 무작위 샘플을 조회한다."""
        ...
