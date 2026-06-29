from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from silicon_valley.adapter.outbound.repositories.piper_gilfoyle_sys_repository import PiperGilfoyleSysQueryRepository
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import PiperGilfoyleSysUseCase
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import PiperGilfoyleSysRepository
from silicon_valley.app.use_cases.piper_gilfoyle_sys_interactor import PiperGilfoyleSysInteractor


def get_piper_gilfoyle_sys_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperGilfoyleSysRepository:
    return PiperGilfoyleSysQueryRepository(session=db)


def get_piper_gilfoyle_sys_use_case(
    repository: PiperGilfoyleSysRepository = Depends(get_piper_gilfoyle_sys_repository),
) -> PiperGilfoyleSysUseCase:
    return PiperGilfoyleSysInteractor(repository=repository)
