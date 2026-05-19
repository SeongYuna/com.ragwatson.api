import logging

from sqlalchemy.ext.asyncio import AsyncSession

from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger(__name__)


class UserController:
    def __init__(self) -> None:
        self.user_service = UserService()

    async def save_user(self, session: AsyncSession, user_schema: UserSchema) -> None:
        await self.user_service.save_user(session, user_schema)
        logger.info("[UserController] save_user 레이어 완료 — userId=%s", user_schema.id)
