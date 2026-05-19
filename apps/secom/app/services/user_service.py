import logging

from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def save_user(self, session: AsyncSession, user_schema: UserSchema) -> None:
        await self.user_repository.save_user(session, user_schema)
        logger.info("[UserService] save_user 레이어 완료 — userId=%s", user_schema.id)
