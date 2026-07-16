from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic_machine_learning.adapter.outbound.database import get_titanic_db

from titanic_machine_learning.adapter.outbound.repositories.lowe_query_repository import LoweQueryRepository
from titanic_machine_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_machine_learning.app.ports.output.lowe_port import LowePort
from titanic_machine_learning.app.use_cases.lowe_query_interactor import LoweQueryInteractor


def get_lowe_repository(
        db: AsyncSession = Depends(get_titanic_db)
) -> LowePort:
    return LoweQueryRepository(db=db)


def get_lowe_use_case(
    repository: LowePort = Depends(get_lowe_repository)
) -> LoweUseCase:
    return LoweQueryInteractor(repository=repository)
