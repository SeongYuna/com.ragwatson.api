from __future__ import annotations

from abc import ABC, abstractmethod


class TelegramNotifierPort(ABC):
    @abstractmethod
    async def send(self, message: str) -> bool:
        ...
