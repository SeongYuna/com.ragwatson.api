from __future__ import annotations

from pydantic import BaseModel


class CommandRequest(BaseModel):
    text: str


class CommandResponse(BaseModel):
    action: str
    websites: list[str]
    keywords: list[str]
    count: int
    saved_files: list[str]
