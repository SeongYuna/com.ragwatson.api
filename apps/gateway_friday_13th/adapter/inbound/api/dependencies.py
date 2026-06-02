from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from gateway_friday_13th.adapter.outbound.pg.user_pg_repository import UserPgRepository
from gateway_friday_13th.app.ports.input.user_cmd_use_case import UserCmdUseCase
from gateway_friday_13th.app.use_cases.user_signup_interactor import UserSignupInteractor


def get_user_cmd_use_case(db: AsyncSession = Depends(get_db)) -> UserCmdUseCase:
    return UserSignupInteractor(repository=UserPgRepository(db))
