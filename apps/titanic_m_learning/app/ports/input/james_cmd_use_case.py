from abc import ABC, abstractmethod

from titanic_m_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesWritePassengerRequest
from titanic_m_learning.app.dtos.james_cmd_dto import JamesUploadResult
from titanic_m_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesIntroduceResponse, JamesIntroduceSchema


class JamesCmdUseCase(ABC):
    @abstractmethod
    async def execute(self, requests: list[JamesWritePassengerRequest]) -> JamesUploadResult:
        """JamesWritePassengerRequest 목록을 Person/Booking 커맨드로 저장한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, schema: JamesIntroduceSchema) -> JamesIntroduceResponse:
        """James 자기소개."""
        ...

