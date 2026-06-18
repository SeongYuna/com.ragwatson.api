from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.caledon_stats_pg_repository import CaledonStatsPgRepository
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.output.caledon_repository import CaledonRepository
from titanic_m_learning.app.use_cases.caledon_query_interactor import CaledonQueryInteractor


def get_caledon_repository(
        db: AsyncSession = Depends(get_db)
) -> CaledonRepository:
    return CaledonStatsPgRepository(session=db)


def get_caledon_use_case(
    repository: CaledonRepository = Depends(get_caledon_repository)
) -> CaledonUseCase:
    return CaledonQueryInteractor(repository=repository)
