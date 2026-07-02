from __future__ import annotations

import os

import httpx

from teaching_assistant_spoke.app.ports.output.email_sender_port import EmailSenderPort

_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/email-send")


class N8nWebhookAdapter(EmailSenderPort):
    """n8n Webhook을 통해 Gmail로 이메일을 발송하는 Secondary Adapter."""

    def __init__(self, webhook_url: str = _WEBHOOK_URL) -> None:
        self._webhook_url = webhook_url

    async def send(self, to: str, subject: str, body: str) -> bool:
        payload = {"to": to, "subject": subject, "body": body}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(self._webhook_url, json=payload)
            return response.status_code == 200
