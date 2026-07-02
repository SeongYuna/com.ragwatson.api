from __future__ import annotations

from abc import ABC, abstractmethod

from teaching_assistant_spoke.app.dtos.receiver_dto import (
    EmailReceivedCommand,
    EmailReceivedResult,
)


class ReceiverUseCase(ABC):
    @abstractmethod
    async def receive(self, command: EmailReceivedCommand) -> EmailReceivedResult:
        ...
