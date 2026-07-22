from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import AuthAccountORM

logger = logging.getLogger(__name__)


async def get_by_id(db: AsyncSession, account_id: str) -> AuthAccountORM | None:
    stmt = select(AuthAccountORM).where(AuthAccountORM.id == account_id)
    return (await db.execute(stmt)).scalar_one_or_none()


async def get_or_create_by_provider(
    db: AsyncSession,
    *,
    provider: str,
    provider_user_id: str,
    email: str | None,
    nickname: str | None,
) -> AuthAccountORM:
    stmt = select(AuthAccountORM).where(
        AuthAccountORM.provider == provider,
        AuthAccountORM.provider_user_id == provider_user_id,
    )
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing is not None:
        return existing

    account = AuthAccountORM(
        email=email,
        nickname=nickname,
        provider=provider,
        provider_user_id=provider_user_id,
    )
    db.add(account)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        logger.warning("[auth] 동시 가입 충돌, 재조회 — provider=%s", provider)
        existing = (await db.execute(stmt)).scalar_one_or_none()
        if existing is not None:
            return existing
        raise ValueError("db:integrity") from exc

    await db.refresh(account)
    return account
