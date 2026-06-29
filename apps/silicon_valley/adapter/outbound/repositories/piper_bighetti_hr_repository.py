from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    PiperBighettiHrIntroduceQuery,
    PiperBighettiHrIntroduceResult,
)
from silicon_valley.app.ports.output.piper_bighetti_hr_port import PiperBighettiHrRepository


class PiperBighettiHrQueryRepository(PiperBighettiHrRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(
        self, query: PiperBighettiHrIntroduceQuery
    ) -> PiperBighettiHrIntroduceResult:
        return PiperBighettiHrIntroduceResult(
            id=query.id,
            name=query.name,
            message="안녕하세요, HR 담당 넬슨 비게티입니다.",
        )
