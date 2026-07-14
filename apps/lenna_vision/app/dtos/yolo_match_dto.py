from __future__ import annotations

from pydantic import BaseModel


class FaceMatchCommand(BaseModel):
    image_bytes: bytes


class CelebrityMatch(BaseModel):
    name: str
    similarity: float  # 0.0 ~ 100.0


class FaceMatchResult(BaseModel):
    matches: list[CelebrityMatch]
    message: str
