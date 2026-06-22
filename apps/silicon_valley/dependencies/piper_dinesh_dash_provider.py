from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.adapter.outbound.pg.piper_dinesh_dash_pg_repository import PiperDineshDashRepository
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import PiperDineshDashUseCase
from silicon_valley.app.ports.output.piper_dinesh_dash_repository import PiperDineshDashRepository
from silicon_valley.app.use_cases.piper_dinesh_dash_interactor import PiperDineshDashInteractor


def get_piper_dinesh_dash_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperDineshDashRepository:
    return PiperDineshDashPgRepository(db=db)


def get_piper_dinesh_dash_use_case(
    repository: PiperDineshDashRepository = Depends(get_piper_dinesh_dash_repository),
) -> PiperDineshDashUseCase:
    return PiperDineshDashInteractor(repository=repository)
