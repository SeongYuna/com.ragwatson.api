from __future__ import annotations

from fastapi import APIRouter, Depends

from teaching_assistant.adapter.inbound.api.schemas.email_schema import (
    EmailSendRequest,
    EmailSendResponse,
)
from teaching_assistant.app.dtos.email_dto import EmailCommand
from teaching_assistant.app.ports.input.email_port import EmailPort
from teaching_assistant.dependencies.email_provider import get_email_use_case

router = APIRouter(prefix="/teaching-assistant/email", tags=["teaching-assistant"])


@router.post("/send", response_model=EmailSendResponse)
async def send_email(
    body: EmailSendRequest,
    use_case: EmailPort = Depends(get_email_use_case),
) -> EmailSendResponse:
    command = EmailCommand(to=body.to, topic=body.topic, tone=body.tone)
    result = await use_case.send_email(command)
    return EmailSendResponse(
        to=result.to,
        subject=result.subject,
        body=result.body,
        sent=result.sent,
    )
