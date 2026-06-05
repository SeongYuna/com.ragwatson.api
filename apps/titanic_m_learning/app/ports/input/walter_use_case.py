from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.table_query_result import TableQueryResult


class WalterUseCase(ABC):
    @abstractmethod
    async def find_all(self) -> TableQueryResult:
        """전체 탑승객 목록을 Person/Booking Query DTO로 조회한다."""
        ...
