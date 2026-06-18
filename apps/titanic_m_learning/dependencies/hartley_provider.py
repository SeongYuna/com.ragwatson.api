from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.hartley_query_pg_repository import HartleyQueryPgRepository
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.hartley_repository import HartleyRepository
from titanic_m_learning.app.use_cases.hartley_query_interactor import HartleyQueryInteractor


def get_hartley_repository(
        db: AsyncSession = Depends(get_db)
) -> HartleyRepository:
    return HartleyQueryPgRepository(session=db)


def get_hartley_use_case(
    repository: HartleyRepository = Depends(get_hartley_repository)
) -> HartleyUseCase:
    return HartleyQueryInteractor(repository=repository)
