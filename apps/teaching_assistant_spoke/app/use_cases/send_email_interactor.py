from __future__ import annotations

from core.lol.orchestrator_port import (
    OrchestratorMessage,
    OrchestratorPort,
    OrchestratorRequest,
)
from teaching_assistant_spoke.app.dtos.email_dto import EmailCommand, EmailResult
from teaching_assistant_spoke.app.ports.input.email_port import EmailPort
from teaching_assistant_spoke.app.ports.output.email_sender_port import EmailSenderPort

_SYSTEM_PROMPT = (
    "당신은 친절하고 전문적인 교육 보조 AI입니다. "
    "주어진 주제와 말투로 이메일 제목과 본문을 작성하세요. "
    "반드시 다음 형식으로만 응답하세요:\n"
    "제목: <이메일 제목>\n"
    "본문:\n<이메일 본문>"
)


class SendEmailInteractor(EmailPort):
    def __init__(
        self,
        orchestrator: OrchestratorPort,
        sender: EmailSenderPort,
    ) -> None:
        self._orchestrator = orchestrator
        self._sender = sender

    async def send_email(self, command: EmailCommand) -> EmailResult:
        # 1. Exaone으로 이메일 본문 생성
        request = OrchestratorRequest(
            messages=[
                OrchestratorMessage(role="system", content=_SYSTEM_PROMPT),
                OrchestratorMessage(
                    role="user",
                    content=f"주제: {command.topic}\n말투: {command.tone}",
                ),
            ]
        )
        response = await self._orchestrator.chat(request)

        # 2. 응답 파싱 (제목 / 본문 분리)
        subject, body = self._parse(response.content, command.topic)

        # 3. n8n Webhook으로 발송
        sent = await self._sender.send(to=command.to, subject=subject, body=body)

        return EmailResult(to=command.to, subject=subject, body=body, sent=sent)

    @staticmethod
    def _parse(content: str, fallback_topic: str) -> tuple[str, str]:
        subject = f"[교육] {fallback_topic}"
        body = content
        for line in content.splitlines():
            if line.startswith("제목:"):
                subject = line.removeprefix("제목:").strip()
            elif line.startswith("본문:"):
                idx = content.index("본문:")
                body = content[idx + len("본문:"):].strip()
                break
        return subject, body
