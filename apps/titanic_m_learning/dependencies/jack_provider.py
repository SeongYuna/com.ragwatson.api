from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.jack_query_pg_repository import JackQueryPgRepository
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.output.jack_repository import JackRepository
from titanic_m_learning.app.use_cases.jack_query_interactor import JackQueryInteractor


def get_jack_use_case(db: AsyncSession = Depends(get_db)) -> JackUseCase:
    repository: JackRepository = JackQueryPgRepository(db=db)
    return JackQueryInteractor(repository=repository)
