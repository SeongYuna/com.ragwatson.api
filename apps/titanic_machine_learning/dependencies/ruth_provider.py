from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic_machine_learning.adapter.outbound.database import get_titanic_db

from titanic_machine_learning.adapter.outbound.repositories.ruth_query_repository import RuthQueryRepository
from titanic_machine_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_machine_learning.app.ports.output.ruth_port import RuthPort
from titanic_machine_learning.app.use_cases.ruth_query_interactor import RuthQueryInteractor


def get_ruth_repository(
        db: AsyncSession = Depends(get_titanic_db)
) -> RuthPort:
    return RuthQueryRepository(db=db)


def get_ruth_use_case(
    repository: RuthPort = Depends(get_ruth_repository)
) -> RuthUseCase:
    return RuthQueryInteractor(repository=repository)
