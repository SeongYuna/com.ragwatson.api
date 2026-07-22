from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class AuthAccountORM(Base):
    """OAuth 전용 사용자 저장소. gateway_kingdom_hearts의 users 테이블과는 독립적이다."""

    __tablename__ = "auth_accounts"
    __table_args__ = (
        UniqueConstraint("provider", "provider_user_id", name="uq_auth_accounts_provider_identity"),
    )

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str | None] = mapped_column(nullable=True)
    nickname: Mapped[str | None] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(default="user")
    provider: Mapped[str] = mapped_column()
    provider_user_id: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
