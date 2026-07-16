from __future__ import annotations

from abc import ABC, abstractmethod

from starcraft_hub.app.dtos.command_dto import ExecuteCommandCommand, ExecuteCommandResult


class CommandPort(ABC):
    @abstractmethod
    async def execute(self, command: ExecuteCommandCommand) -> ExecuteCommandResult:
        ...
