from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dunn_coo_dto import (
    PiperDunnCooIntroduceQuery,
    PiperDunnCooIntroduceResult,
)
from silicon_valley.app.ports.output.piper_dunn_coo_repository import PiperDunnCooRepository


class PiperDunnCooPgRepository(PiperDunnCooRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(
        self, query: PiperDunnCooIntroduceQuery
    ) -> PiperDunnCooIntroduceResult:
        return PiperDunnCooIntroduceResult(
            id=query.id,
            name=query.name,
            message='파이드 파이퍼 COO Donald Dunn(Jared)입니다. 누구보다 헌신적으로 회사 운영을 책임집니다.',
        )
