"""시스템 전역 API 키·환경(.env)을 관리하는 KeyMaker."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

_DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)
    model: str | None = None


class KeyMaker:
    """backend/.env 로드 및 Gemini 등 외부 API 자격 증명을 한곳에서 관리합니다."""

    __slots__ = ("_backend_root",)

    def __init__(self, backend_root: Path | None = None) -> None:
        if backend_root is None:
            # .../backend/apps/matrix/app/keymaker.py → backend/
            self._backend_root = Path(__file__).resolve().parent.parent.parent.parent
        else:
            self._backend_root = Path(backend_root)
        self.load_env()

    @property
    def backend_root(self) -> Path:
        return self._backend_root

    def load_env(self) -> None:
        load_dotenv(self._backend_root / ".env")

    def refresh(self) -> None:
        """.env를 다시 읽습니다."""
        self.load_env()

    @property
    def gemini_api_key(self) -> str:
        return (os.getenv("GEMINI_API_KEY", "") or "").strip()

    @property
    def gemini_model_name(self) -> str:
        name = (os.getenv("GEMINI_MODEL_NAME", "") or "").strip()
        return name or _DEFAULT_GEMINI_MODEL

    @property
    def meteo_api_key(self) -> str:
        return (os.getenv("METEO_API_KEY", "") or "").strip()

    def get(self, name: str, default: str = "") -> str:
        """추가 API·설정용 환경 변수 조회."""
        return (os.getenv(name, "") or default).strip()


keymaker = KeyMaker()
