from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from silicon_valley.adapter.outbound.repositories.piper_dunn_coo_repository import PiperDunnCooQueryRepository
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import PiperDunnCooUseCase
from silicon_valley.app.ports.output.piper_dunn_coo_port import PiperDunnCooRepository
from silicon_valley.app.use_cases.piper_dunn_coo_interactor import PiperDunnCooInteractor


def get_piper_dunn_coo_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperDunnCooRepository:
    return PiperDunnCooQueryRepository(session=db)


def get_piper_dunn_coo_use_case(
    repository: PiperDunnCooRepository = Depends(get_piper_dunn_coo_repository),
) -> PiperDunnCooUseCase:
    return PiperDunnCooInteractor(repository=repository)
