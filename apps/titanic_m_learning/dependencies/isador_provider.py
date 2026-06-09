from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.isador_query_pg_repository import IsadorQueryPgRepository
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.ports.output.isador_repository import IsadorRepository
from titanic_m_learning.app.use_cases.isador_query_interactor import IsadorQueryInteractor


def get_isador_use_case(db: AsyncSession = Depends(get_db)) -> IsadorUseCase:
    repository: IsadorRepository = IsadorQueryPgRepository(db=db)
    return IsadorQueryInteractor(repository=repository)
