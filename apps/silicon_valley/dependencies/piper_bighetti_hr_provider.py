from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.adapter.outbound.pg.piper_bighetti_hr_pg_repository import PiperBighettiHrRepository
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import PiperBighettiHrUseCase
from silicon_valley.app.ports.output.piper_bighetti_hr_repository import PiperBighettiHrRepository
from silicon_valley.app.use_cases.piper_bighetti_hr_interactor import PiperBighettiHrInteractor


def get_piper_bighetti_hr_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperBighettiHrRepository:
    return PiperBighettiHrPgRepository(db=db)


def get_piper_bighetti_hr_use_case(
    repository: PiperBighettiHrRepository = Depends(get_piper_bighetti_hr_repository),
) -> PiperBighettiHrUseCase:
    return PiperBighettiHrInteractor(repository=repository)
