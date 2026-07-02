from __future__ import annotations

from pydantic import BaseModel


class EmailReceivedPayload(BaseModel):
    """n8n Gmail 트리거가 전달하는 수신 이메일 데이터."""
    sender: str
    subject: str
    body: str
    received_at: str = ""


class EmailReceivedResponse(BaseModel):
    id: int
    logged: bool
    notified: bool
    embedded: bool
