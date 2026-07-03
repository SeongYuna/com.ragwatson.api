from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lenna_vision.adapter.outbound.repositories.lenna_vision_query_repository import LennaVisionQueryRepository
from lenna_vision.app.ports.input.lenna_vision_use_case import LennaVisionUseCase
from lenna_vision.app.ports.output.lenna_vision_port import LennaVisionPort
from lenna_vision.app.use_cases.lenna_vision_query_interactor import LennaVisionQueryInteractor


def get_lenna_vision_repository(
        db: AsyncSession = Depends(get_db)
) -> LennaVisionPort:
    return LennaVisionQueryRepository(db=db)


def get_lenna_vision_use_case(
    repository: LennaVisionPort = Depends(get_lenna_vision_repository)
) -> LennaVisionUseCase:
    return LennaVisionQueryInteractor(repository=repository)
