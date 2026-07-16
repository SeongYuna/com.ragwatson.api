from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic_machine_learning.adapter.outbound.database import get_titanic_db

from titanic_machine_learning.adapter.outbound.repositories.caledon_stats_repository import CaledonStatsRepository
from titanic_machine_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_machine_learning.app.ports.output.caledon_port import CaledonPort
from titanic_machine_learning.app.use_cases.caledon_query_interactor import CaledonQueryInteractor


def get_caledon_repository(
        db: AsyncSession = Depends(get_titanic_db)
) -> CaledonPort:
    return CaledonStatsRepository(db=db)


def get_caledon_use_case(
    repository: CaledonPort = Depends(get_caledon_repository)
) -> CaledonUseCase:
    return CaledonQueryInteractor(repository=repository)
