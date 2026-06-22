from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.adapter.outbound.pg.piper_dunn_coo_pg_repository import PiperDunnCooRepository
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import PiperDunnCooUseCase
from silicon_valley.app.ports.output.piper_dunn_coo_repository import PiperDunnCooRepository
from silicon_valley.app.use_cases.piper_dunn_coo_interactor import PiperDunnCooInteractor


def get_piper_dunn_coo_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperDunnCooRepository:
    return PiperDunnCooPgRepository(db=db)


def get_piper_dunn_coo_use_case(
    repository: PiperDunnCooRepository = Depends(get_piper_dunn_coo_repository),
) -> PiperDunnCooUseCase:
    return PiperDunnCooInteractor(repository=repository)
