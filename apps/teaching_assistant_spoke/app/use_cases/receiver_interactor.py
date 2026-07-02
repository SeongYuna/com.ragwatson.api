from __future__ import annotations

import logging

from teaching_assistant_spoke.app.dtos.receiver_dto import (
    EmailReceivedCommand,
    EmailReceivedResult,
)
from teaching_assistant_spoke.app.ports.input.receiver_use_case import ReceiverUseCase
from teaching_assistant_spoke.app.ports.output.embedder_port import EmbedderPort
from teaching_assistant_spoke.app.ports.output.email_store_port import EmailStorePort
from teaching_assistant_spoke.app.ports.output.receiver_port import TelegramNotifierPort

logger = logging.getLogger(__name__)


class ReceiverInteractor(ReceiverUseCase):
    def __init__(
        self,
        notifier: TelegramNotifierPort,
        store: EmailStorePort,
        embedder: EmbedderPort,
    ) -> None:
        self._notifier = notifier
        self._store = store
        self._embedder = embedder

    async def receive(self, command: EmailReceivedCommand) -> EmailReceivedResult:
        # 1. 로그 작성
        logger.info(
            "[수신] from=%s | subject=%s | at=%s",
            command.sender,
            command.subject,
            command.received_at,
        )

        # 2. 임베딩 생성 (제목 + 본문 결합)
        embed_text = f"{command.subject}\n{command.body}"
        embedding = await self._embedder.embed(embed_text)

        # 3. pgvector 저장
        saved_id = await self._store.save(command, embedding)
        logger.info("[저장] received_emails.id=%d embedded=True", saved_id)

        # 4. 텔레그램 알림
        message = (
            f"📬 새 이메일 수신\n"
            f"발신: {command.sender}\n"
            f"제목: {command.subject}\n"
            f"수신: {command.received_at}"
        )
        notified = await self._notifier.send(message)

        return EmailReceivedResult(
            id=saved_id,
            logged=True,
            notified=notified,
            embedded=True,
        )
