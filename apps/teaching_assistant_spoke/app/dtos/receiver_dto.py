from __future__ import annotations

from pydantic import BaseModel


class EmailReceivedCommand(BaseModel):
    sender: str
    subject: str
    body: str
    received_at: str = ""


class EmailReceivedResult(BaseModel):
    id: int
    logged: bool
    notified: bool
    embedded: bool
