from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.repositories.lowe_query_repository import LoweQueryRepository
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.output.lowe_port import LowePort
from titanic_m_learning.app.use_cases.lowe_query_interactor import LoweQueryInteractor


def get_lowe_repository(
        db: AsyncSession = Depends(get_db)
) -> LowePort:
    return LoweQueryRepository(db=db)


def get_lowe_use_case(
    repository: LowePort = Depends(get_lowe_repository)
) -> LoweUseCase:
    return LoweQueryInteractor(repository=repository)
