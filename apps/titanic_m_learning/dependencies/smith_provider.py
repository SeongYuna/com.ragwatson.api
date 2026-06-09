from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.smith_stats_pg_repository import SmithStatsPgRepository
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase
from titanic_m_learning.app.ports.output.smith_repository import SmithRepository
from titanic_m_learning.app.use_cases.smith_query_interactor import SmithQueryInteractor


def get_smith_use_case(db: AsyncSession = Depends(get_db)) -> SmithUseCase:
    repository: SmithRepository = SmithStatsPgRepository(db=db)
    return SmithQueryInteractor(repository=repository)
