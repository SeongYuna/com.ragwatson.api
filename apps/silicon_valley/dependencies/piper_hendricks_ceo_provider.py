from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.adapter.outbound.pg.piper_hendricks_ceo_pg_repository import PiperHendricksCeoPgRepository
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import PiperHendricksCeoUseCase
from silicon_valley.app.ports.output.piper_hendricks_ceo_repository import PiperHendricksCeoRepository
from silicon_valley.app.use_cases.piper_hendricks_ceo_interactor import PiperHendricksCeoInteractor


def get_piper_hendricks_ceo_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperHendricksCeoRepository:
    return PiperHendricksCeoPgRepository(db=db)


def get_piper_hendricks_ceo_use_case(
    repository: PiperHendricksCeoRepository = Depends(get_piper_hendricks_ceo_repository),
) -> PiperHendricksCeoUseCase:
    return PiperHendricksCeoInteractor(repository=repository)
