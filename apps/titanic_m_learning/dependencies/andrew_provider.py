from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.andrew_query_pg_repository import AndrewQueryPgRepository
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.app.ports.output.andrew_repository import AndrewRepository
from titanic_m_learning.app.use_cases.andrew_query_interactor import AndrewQueryInteractor


def get_andrew_repository(
        db: AsyncSession = Depends(get_db)
) -> AndrewRepository:
    return AndrewQueryPgRepository(session=db)


def get_andrew_use_case(
    repository: AndrewRepository = Depends(get_andrew_repository)
) -> AndrewUseCase:
    return AndrewQueryInteractor(repository=repository)
