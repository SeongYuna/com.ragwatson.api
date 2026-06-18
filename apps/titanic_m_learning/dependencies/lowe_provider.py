from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.lowe_query_pg_repository import LoweQueryPgRepository
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.output.lowe_repository import LoweRepository
from titanic_m_learning.app.use_cases.lowe_query_interactor import LoweQueryInteractor


def get_lowe_repository(
        db: AsyncSession = Depends(get_db)
) -> LoweRepository:
    return LoweQueryPgRepository(session=db)


def get_lowe_use_case(
    repository: LoweRepository = Depends(get_lowe_repository)
) -> LoweUseCase:
    return LoweQueryInteractor(repository=repository)
