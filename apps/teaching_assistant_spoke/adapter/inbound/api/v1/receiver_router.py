from __future__ import annotations

from fastapi import APIRouter, Depends

from teaching_assistant_spoke.adapter.inbound.api.schemas.receiver_schema import (
    EmailReceivedPayload,
    EmailReceivedResponse,
)
from teaching_assistant_spoke.app.dtos.receiver_dto import EmailReceivedCommand
from teaching_assistant_spoke.app.ports.input.receiver_use_case import ReceiverUseCase
from teaching_assistant_spoke.dependencies.reciever_provider import get_receiver_use_case

router = APIRouter(prefix="/teaching-assistant/receiver", tags=["teaching-assistant"])


@router.post("/email", response_model=EmailReceivedResponse)
async def receive_email(
    payload: EmailReceivedPayload,
    use_case: ReceiverUseCase = Depends(get_receiver_use_case),
) -> EmailReceivedResponse:
    """n8n Gmail 트리거 → 로그 + 임베딩(pgvector 저장) + 텔레그램 알림."""
    command = EmailReceivedCommand(
        sender=payload.sender,
        subject=payload.subject,
        body=payload.body,
        received_at=payload.received_at,
    )
    result = await use_case.receive(command)
    return EmailReceivedResponse(
        id=result.id,
        logged=result.logged,
        notified=result.notified,
        embedded=result.embedded,
    )
