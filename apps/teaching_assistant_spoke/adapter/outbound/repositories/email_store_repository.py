from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from teaching_assistant_spoke.adapter.outbound.orm.received_email_orm import ReceivedEmailORM
from teaching_assistant_spoke.app.dtos.receiver_dto import EmailReceivedCommand
from teaching_assistant_spoke.app.ports.output.email_store_port import EmailStorePort


class EmailStorePgRepository(EmailStorePort):
    """Jack 패턴 참조 — AsyncSession 주입, ORM 직접 조작."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(
        self,
        command: EmailReceivedCommand,
        embedding: list[float] | None,
    ) -> int:
        row = ReceivedEmailORM(
            sender=command.sender,
            subject=command.subject,
            body=command.body,
            received_at=command.received_at,
            embedding=embedding,
        )
        self._session.add(row)
        await self._session.flush()   # id 확보
        await self._session.commit()
        return row.id
