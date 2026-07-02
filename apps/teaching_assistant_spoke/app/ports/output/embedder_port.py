from __future__ import annotations

from abc import ABC, abstractmethod


class EmbedderPort(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """텍스트를 384차원 벡터로 변환한다."""
        ...
