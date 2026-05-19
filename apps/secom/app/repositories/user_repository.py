import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.models.user_model import User
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserRepository:
    async def save_user(self, session: AsyncSession, user_schema: UserSchema) -> None:
        user = User(
            id=user_schema.id,
            password=user_schema.password,
            nickname=user_schema.nickname,
            email=user_schema.email,
            role=user_schema.role,
        )
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as e:
            await session.rollback()
            err_name = type(e.orig).__name__ if e.orig else ""
            err_detail = str(e.orig) if e.orig else str(e)
            logger.error(
                "[UserRepository] INSERT 실패 — %s: %s",
                err_name or "IntegrityError",
                err_detail,
            )
            if err_name == "UniqueViolation":
                raise ValueError("duplicate") from e
            if err_name == "NotNullViolation":
                raise ValueError("schema") from e
            raise ValueError(f"db:{err_name or 'integrity'}:{err_detail}") from e
        logger.info("[UserRepository] save_user 레이어 완료 — userId=%s", user_schema.id)
