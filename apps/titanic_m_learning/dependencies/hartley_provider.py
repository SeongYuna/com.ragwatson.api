from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.hartley_query_pg_repository import HartleyQueryPgRepository
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.hartley_repository import HartleyRepository
from titanic_m_learning.app.use_cases.hartley_query_interactor import HartleyQueryInteractor


def get_hartley_use_case(db: AsyncSession = Depends(get_db)) -> HartleyUseCase:
    repository: HartleyRepository = HartleyQueryPgRepository(db=db)
    return HartleyQueryInteractor(repository=repository)
