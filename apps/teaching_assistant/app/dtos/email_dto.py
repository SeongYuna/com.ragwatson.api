from __future__ import annotations

from pydantic import BaseModel, EmailStr


class EmailCommand(BaseModel):
    to: EmailStr
    topic: str
    tone: str = "친근하게"


class EmailResult(BaseModel):
    to: str
    subject: str
    body: str
    sent: bool
