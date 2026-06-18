from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.james_cmd_dto import (
    JamesPassengerCommand,
    JamesUploadResult,
    JamesIntroduceQuery,
    JamesIntroduceResult,
)


class JamesCmdUseCase(ABC):
    @abstractmethod
    async def execute(self, commands: list[JamesPassengerCommand]) -> JamesUploadResult:
        """JamesPassengerCommand 목록을 Person/Booking 커맨드로 저장한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, query: JamesIntroduceQuery) -> JamesIntroduceResult:
        """James 자기소개."""
        ...
