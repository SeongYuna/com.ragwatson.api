import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from gateway_kingdom_hearts.adapter.outbound.mappers.user_orm_mapper import user_to_orm
from gateway_kingdom_hearts.app.ports.output.user_repository import UserRepository
from gateway_kingdom_hearts.domain.entities.user import User

logger = logging.getLogger(__name__)


class UserPgRepository(UserRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save(self, user: User) -> None:
        self._db.add(user_to_orm(user))
        try:
            await self._db.commit()
        except IntegrityError as exc:
            await self._db.rollback()
            err_name = type(exc.orig).__name__ if exc.orig else ""
            err_detail = str(exc.orig) if exc.orig else str(exc)
            logger.error(
                "[UserPgRepository] INSERT 실패 — %s: %s",
                err_name or "IntegrityError",
                err_detail,
            )
            if err_name == "UniqueViolation":
                raise ValueError("duplicate") from exc
            if err_name == "NotNullViolation":
                raise ValueError("schema") from exc
            raise ValueError(f"db:{err_name or 'integrity'}:{err_detail}") from exc
        logger.info("[UserPgRepository] save 완료 — userId=%s", user.id)
