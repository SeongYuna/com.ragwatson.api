from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.james_cmd_dto import JamesPassengerCommand
from titanic_machine_learning.app.dtos.james_cmd_dto import JamesIntroduceQuery, JamesIntroduceResult


class JamesCmdPort(ABC):
    @abstractmethod
    async def save_all(self, commands: list[JamesPassengerCommand]) -> None:
        """PersonCommand + BookingCommand 목록을 저장소에 저장한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, query: JamesIntroduceQuery) -> JamesIntroduceResult:
        ...

