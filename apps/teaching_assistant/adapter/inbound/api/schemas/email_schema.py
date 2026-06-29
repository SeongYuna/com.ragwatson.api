from __future__ import annotations

from pydantic import BaseModel, EmailStr


class EmailSendRequest(BaseModel):
    to: EmailStr
    topic: str
    tone: str = "친근하게"


class EmailSendResponse(BaseModel):
    to: str
    subject: str
    body: str
    sent: bool
