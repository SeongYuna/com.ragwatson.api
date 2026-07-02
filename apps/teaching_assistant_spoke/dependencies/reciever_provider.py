from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from teaching_assistant_spoke.adapter.outbound.repositories.email_store_repository import (
    EmailStorePgRepository,
)
from teaching_assistant_spoke.adapter.outbound.repositories.reciever_repository import (
    TelegramNotifierAdapter,
)
from teaching_assistant_spoke.adapter.outbound.repositories.sentence_embedder import (
    SentenceEmbedderAdapter,
)
from teaching_assistant_spoke.app.ports.input.receiver_use_case import ReceiverUseCase
from teaching_assistant_spoke.app.use_cases.receiver_interactor import ReceiverInteractor


def get_receiver_use_case(
    db: AsyncSession = Depends(get_db),
) -> ReceiverUseCase:
    return ReceiverInteractor(
        notifier=TelegramNotifierAdapter(),
        store=EmailStorePgRepository(session=db),
        embedder=SentenceEmbedderAdapter(),
    )
