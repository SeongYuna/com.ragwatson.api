from __future__ import annotations

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from core.database import Base


class ReceivedEmailORM(Base):
    """n8n Gmail 트리거로 수신된 이메일 + pgvector 임베딩."""

    __tablename__ = "received_emails"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sender: Mapped[str] = mapped_column(String(320), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
