from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from gateway_kingdom_hearts.adapter.outbound.pg.user_pg_repository import UserRepository
from gateway_kingdom_hearts.app.ports.input.user_cmd_use_case import UserCmdUseCase
from gateway_kingdom_hearts.app.use_cases.user_signup_interactor import UserSignupInteractor


def get_user_cmd_use_case(db: AsyncSession = Depends(get_db)) -> UserCmdUseCase:
    return UserSignupInteractor(repository=UserPgRepository(db))
