from __future__ import annotations

from pydantic import BaseModel


class ExecuteCommandCommand(BaseModel):
    text: str


class ExecuteCommandResult(BaseModel):
    action: str
    websites: list[str]
    keywords: list[str]
    count: int
    saved_files: list[str]
