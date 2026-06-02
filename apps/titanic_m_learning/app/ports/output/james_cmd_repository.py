from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.james_cmd_dto import JamesPassengerCommand


class JamesCmdRepository(ABC):
    @abstractmethod
    async def save_all(self, commands: list[JamesPassengerCommand]) -> None:
        """PersonCommand + BookingCommand 목록을 저장소에 저장한다."""
        ...
