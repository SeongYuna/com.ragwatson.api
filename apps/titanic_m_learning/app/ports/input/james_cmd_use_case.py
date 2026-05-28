from abc import ABC, abstractmethod

from titanic_m_learning.app.dto.upload_result import UploadResult
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class JamesCmdUseCase(ABC):
    @abstractmethod
    async def execute(self, passengers: list[TitanicPassenger]) -> UploadResult:
        """도메인 탑승객 목록을 저장한다."""
        ...
