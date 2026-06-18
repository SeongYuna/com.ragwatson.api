from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.rose_query_pg_repository import RoseQueryPgRepository
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.output.rose_repository import RoseRepository
from titanic_m_learning.app.use_cases.rose_query_interactor import RoseQueryInteractor


def get_rose_repository(
        db: AsyncSession = Depends(get_db)
) -> RoseRepository:
    return RoseQueryPgRepository(session=db)


def get_rose_use_case(
    repository: RoseRepository = Depends(get_rose_repository)
) -> RoseUseCase:
    return RoseQueryInteractor(repository=repository)
