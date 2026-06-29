from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.adapter.outbound.repositories.molly_query_repository import MollyQueryRepository
from titanic_machine_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_machine_learning.app.ports.output.molly_port import MollyPort
from titanic_machine_learning.app.use_cases.molly_query_interactor import MollyQueryInteractor


def get_molly_repository(
        db: AsyncSession = Depends(get_db)
) -> MollyPort:
    return MollyQueryRepository(db=db)


def get_molly_use_case(
    repository: MollyPort = Depends(get_molly_repository)
) -> MollyUseCase:
    return MollyQueryInteractor(repository=repository)
