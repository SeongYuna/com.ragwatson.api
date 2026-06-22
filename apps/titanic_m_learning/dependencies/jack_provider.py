from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.repositories.jack_query_repository import JackQueryRepository
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.output.jack_port import JackPort
from titanic_m_learning.app.use_cases.jack_query_interactor import JackQueryInteractor
from titanic_m_learning.dependencies.lowe_provider import get_lowe_use_case
from titanic_m_learning.dependencies.rose_provider import get_rose_use_case


def get_jack_repository(
        db: AsyncSession = Depends(get_db)
) -> JackPort:
    return JackQueryRepository(db=db)


def get_jack_use_case(
    repository: JackPort = Depends(get_jack_repository),
    lowe: LoweUseCase = Depends(get_lowe_use_case),
    rose: RoseUseCase = Depends(get_rose_use_case),
) -> JackUseCase:
    return JackQueryInteractor(repository=repository, lowe=lowe, rose=rose)
