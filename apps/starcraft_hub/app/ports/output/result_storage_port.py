from __future__ import annotations

from abc import ABC, abstractmethod


class ResultStoragePort(ABC):
    @abstractmethod
    async def save(self, filename: str, content: str) -> str:
        ...
