from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.molly_query_pg_repository import MollyQueryPgRepository
from titanic_m_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_m_learning.app.ports.output.molly_repository import MollyRepository
from titanic_m_learning.app.use_cases.molly_query_interactor import MollyQueryInteractor


def get_molly_repository(
        db: AsyncSession = Depends(get_db)
) -> MollyRepository:
    return MollyQueryPgRepository(session=db)


def get_molly_use_case(
    repository: MollyRepository = Depends(get_molly_repository)
) -> MollyUseCase:
    return MollyQueryInteractor(repository=repository)
