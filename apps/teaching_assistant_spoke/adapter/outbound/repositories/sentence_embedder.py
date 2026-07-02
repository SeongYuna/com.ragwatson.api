from __future__ import annotations

import os

import ollama

from teaching_assistant_spoke.app.ports.output.embedder_port import EmbedderPort

_OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
_EMBED_MODEL = "nomic-embed-text"


class SentenceEmbedderAdapter(EmbedderPort):
    """nomic-embed-text (Ollama) — 768차원 임베딩."""

    def __init__(self) -> None:
        self._client = ollama.AsyncClient(host=_OLLAMA_HOST)

    async def embed(self, text: str) -> list[float]:
        response = await self._client.embed(model=_EMBED_MODEL, input=text)
        return response.embeddings[0]
