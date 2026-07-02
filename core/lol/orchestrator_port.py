from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator

from pydantic import BaseModel, Field

_DEFAULT_MODEL = "exaone3.5:2.4b"


class OrchestratorMessage(BaseModel):
    role: str
    content: str


class OrchestratorRequest(BaseModel):
    messages: list[OrchestratorMessage] = Field(..., min_length=1)
    model: str = _DEFAULT_MODEL
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class OrchestratorResponse(BaseModel):
    content: str
    model: str
    done: bool = True


class OrchestratorPort(ABC):
    @abstractmethod
    async def chat(self, request: OrchestratorRequest) -> OrchestratorResponse:
        ...

    @abstractmethod
    async def stream(self, request: OrchestratorRequest) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def ping(self) -> bool:
        ...
