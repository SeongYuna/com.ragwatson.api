from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    PiperBighettiHrIntroduceQuery,
    PiperBighettiHrIntroduceResult,
)
from silicon_valley.app.ports.output.piper_bighetti_hr_repository import PiperBighettiHrRepository


class PiperBighettiHrPgRepository(PiperBighettiHrRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(
        self, query: PiperBighettiHrIntroduceQuery
    ) -> PiperBighettiHrIntroduceResult:
        return PiperBighettiHrIntroduceResult(
            id=query.id,
            name=query.name,
            message='공동창업자 Nelson Bighetti(Big Head)입니다. 운 좋게도 항상 좋은 자리에 있습니다.',
        )
