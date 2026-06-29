from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dunn_coo_dto import (
    PiperDunnCooIntroduceQuery,
    PiperDunnCooIntroduceResult,
)
from silicon_valley.app.ports.output.piper_dunn_coo_port import PiperDunnCooRepository


class PiperDunnCooQueryRepository(PiperDunnCooRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(
        self, query: PiperDunnCooIntroduceQuery
    ) -> PiperDunnCooIntroduceResult:
        return PiperDunnCooIntroduceResult(
            id=query.id,
            name=query.name,
            message="안녕하세요, Pied Piper COO 도널드 던입니다.",
        )
