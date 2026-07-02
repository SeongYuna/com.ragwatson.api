from __future__ import annotations

from pydantic import BaseModel


class ClassifyEmailCommand(BaseModel):
    subject: str
    body: str
    sender: str = ""


class ClassifyEmailResult(BaseModel):
    is_spam: bool
    category: str
    confidence: str
    score: float
    reasoning: str
