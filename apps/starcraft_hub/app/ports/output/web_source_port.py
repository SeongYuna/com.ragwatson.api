from __future__ import annotations

from abc import ABC, abstractmethod


class WebSourcePort(ABC):
    @abstractmethod
    async def get_websites(self) -> list[str]:
        ...

    @abstractmethod
    async def get_keywords(self) -> list[str]:
        ...
