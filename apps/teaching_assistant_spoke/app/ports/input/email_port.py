from __future__ import annotations

from abc import ABC, abstractmethod

from teaching_assistant_spoke.app.dtos.email_dto import EmailCommand, EmailResult


class EmailPort(ABC):
    @abstractmethod
    async def send_email(self, command: EmailCommand) -> EmailResult:
        ...
