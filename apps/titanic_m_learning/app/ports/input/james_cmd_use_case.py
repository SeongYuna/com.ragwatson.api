from abc import ABC, abstractmethod

from titanic_m_learning.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRequest
from titanic_m_learning.app.dtos.upload_result import UploadResult


class JamesCmdUseCase(ABC):
    @abstractmethod
    async def execute(self, requests: list[TitanicPassengerRequest]) -> UploadResult:
        """TitanicPassengerRequest 목록을 Person/Booking 커맨드로 저장한다."""
        ...
