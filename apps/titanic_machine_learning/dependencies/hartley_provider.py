from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.adapter.outbound.repositories.hartley_query_repository import HartleyQueryRepository
from titanic_machine_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_machine_learning.app.ports.output.hartley_port import HartleyPort
from titanic_machine_learning.app.use_cases.hartley_query_interactor import HartleyQueryInteractor


def get_hartley_repository(
        db: AsyncSession = Depends(get_db)
) -> HartleyPort:
    return HartleyQueryRepository(db=db)


def get_hartley_use_case(
    repository: HartleyPort = Depends(get_hartley_repository)
) -> HartleyUseCase:
    return HartleyQueryInteractor(repository=repository)
