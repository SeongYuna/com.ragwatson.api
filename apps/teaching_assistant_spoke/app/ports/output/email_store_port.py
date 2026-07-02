from __future__ import annotations

from abc import ABC, abstractmethod

from teaching_assistant_spoke.app.dtos.receiver_dto import EmailReceivedCommand


class EmailStorePort(ABC):
    @abstractmethod
    async def save(self, command: EmailReceivedCommand, embedding: list[float] | None) -> int:
        """수신 이메일을 embedding과 함께 저장한다. 저장된 row id 반환."""
        ...
