from __future__ import annotations

from pydantic import BaseModel


class ClassifyRequest(BaseModel):
    subject: str
    body: str
    sender: str = ""


class ClassifyResponse(BaseModel):
    is_spam: bool
    category: str
    confidence: str
    score: float
    reasoning: str
