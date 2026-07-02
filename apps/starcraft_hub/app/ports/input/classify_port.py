from __future__ import annotations

from abc import ABC, abstractmethod

from starcraft_hub.app.dtos.classify_dto import ClassifyEmailCommand, ClassifyEmailResult


class ClassifyPort(ABC):
    @abstractmethod
    async def classify(self, command: ClassifyEmailCommand) -> ClassifyEmailResult:
        ...
