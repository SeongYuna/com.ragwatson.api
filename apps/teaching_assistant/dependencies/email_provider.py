from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import faker_orchestrator
from teaching_assistant.adapter.outbound.n8n.n8n_webhook_adapter import N8nWebhookAdapter
from teaching_assistant.app.ports.input.email_port import EmailPort
from teaching_assistant.app.use_cases.send_email_interactor import SendEmailInteractor


def get_email_use_case() -> EmailPort:
    return SendEmailInteractor(
        orchestrator=faker_orchestrator,
        sender=N8nWebhookAdapter(),
    )
