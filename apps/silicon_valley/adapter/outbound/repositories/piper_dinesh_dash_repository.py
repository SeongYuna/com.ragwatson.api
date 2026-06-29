from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dinesh_dash_dto import (
    PiperDineshDashIntroduceQuery,
    PiperDineshDashIntroduceResult,
)
from silicon_valley.app.ports.output.piper_dinesh_dash_port import PiperDineshDashRepository


class PiperDineshDashQueryRepository(PiperDineshDashRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(
        self, query: PiperDineshDashIntroduceQuery
    ) -> PiperDineshDashIntroduceResult:
        return PiperDineshDashIntroduceResult(
            id=query.id,
            name=query.name,
            message="안녕하세요, 개발자 디네시 추그타이입니다.",
        )
