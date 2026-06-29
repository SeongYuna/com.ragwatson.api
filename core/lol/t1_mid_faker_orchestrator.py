"""T1 Mid Faker Orchestrator — Exaone 3.5:2.4b (Ollama) 로컬 오케스트레이터."""

from __future__ import annotations

from typing import AsyncIterator

import ollama
from pydantic import BaseModel, Field

_DEFAULT_MODEL = "exaone3.5:2.4b"
_DEFAULT_HOST = "http://localhost:11434"


class OrchestratorMessage(BaseModel):
    role: str  # "system" | "user" | "assistant"
    content: str


class OrchestratorRequest(BaseModel):
    messages: list[OrchestratorMessage] = Field(..., min_length=1)
    model: str = _DEFAULT_MODEL
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class OrchestratorResponse(BaseModel):
    content: str
    model: str
    done: bool = True


class FakerOrchestrator:
    """Exaone 3.5:2.4b를 Ollama를 통해 실행하는 로컬 LLM 오케스트레이터."""

    def __init__(
        self,
        host: str = _DEFAULT_HOST,
        model: str = _DEFAULT_MODEL,
    ) -> None:
        self._model = model
        self._client = ollama.AsyncClient(host=host)

    @property
    def model(self) -> str:
        return self._model

    async def chat(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """단일 응답을 반환한다."""
        response = await self._client.chat(
            model=request.model,
            messages=[m.model_dump() for m in request.messages],
            options={"temperature": request.temperature},
        )
        return OrchestratorResponse(
            content=response.message.content or "",
            model=response.model or _DEFAULT_MODEL,
            done=response.done or False,
        )

    async def stream(
        self, request: OrchestratorRequest
    ) -> AsyncIterator[str]:
        """청크 단위로 스트리밍한다."""
        async for chunk in await self._client.chat(
            model=request.model,
            messages=[m.model_dump() for m in request.messages],
            options={"temperature": request.temperature},
            stream=True,
        ):
            if chunk.message.content:
                yield chunk.message.content

    async def ping(self) -> bool:
        """Ollama 서버 연결 확인."""
        try:
            await self._client.list()
            return True
        except Exception:
            return False


# 싱글턴 — 앱 전반에서 재사용
faker_orchestrator = FakerOrchestrator()
