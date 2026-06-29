from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from silicon_valley.adapter.outbound.repositories.piper_dinesh_dash_repository import PiperDineshDashQueryRepository
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import PiperDineshDashUseCase
from silicon_valley.app.ports.output.piper_dinesh_dash_port import PiperDineshDashRepository
from silicon_valley.app.use_cases.piper_dinesh_dash_interactor import PiperDineshDashInteractor


def get_piper_dinesh_dash_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperDineshDashRepository:
    return PiperDineshDashQueryRepository(session=db)


def get_piper_dinesh_dash_use_case(
    repository: PiperDineshDashRepository = Depends(get_piper_dinesh_dash_repository),
) -> PiperDineshDashUseCase:
    return PiperDineshDashInteractor(repository=repository)
