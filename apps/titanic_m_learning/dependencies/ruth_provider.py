from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.ruth_query_pg_repository import RuthQueryPgRepository
from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_m_learning.app.ports.output.ruth_repository import RuthRepository
from titanic_m_learning.app.use_cases.ruth_query_interactor import RuthQueryInteractor


def get_ruth_repository(
        db: AsyncSession = Depends(get_db)
) -> RuthRepository:
    return RuthQueryPgRepository(session=db)


def get_ruth_use_case(
    repository: RuthRepository = Depends(get_ruth_repository)
) -> RuthUseCase:
    return RuthQueryInteractor(repository=repository)
