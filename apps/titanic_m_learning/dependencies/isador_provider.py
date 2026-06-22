from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.repositories.isador_query_repository import IsadorQueryRepository
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.ports.output.isador_port import IsadorPort
from titanic_m_learning.app.use_cases.isador_query_interactor import IsadorQueryInteractor


def get_isador_repository(
        db: AsyncSession = Depends(get_db)
) -> IsadorPort:
    return IsadorQueryRepository(db=db)


def get_isador_use_case(
    repository: IsadorPort = Depends(get_isador_repository)
) -> IsadorUseCase:
    return IsadorQueryInteractor(repository=repository)
