from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dinesh_dash_dto import (
    PiperDineshDashIntroduceQuery,
    PiperDineshDashIntroduceResult,
)
from silicon_valley.app.ports.output.piper_dinesh_dash_repository import PiperDineshDashRepository


class PiperDineshDashPgRepository(PiperDineshDashRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(
        self, query: PiperDineshDashIntroduceQuery
    ) -> PiperDineshDashIntroduceResult:
        return PiperDineshDashIntroduceResult(
            id=query.id,
            name=query.name,
            message='백엔드 개발자 Dinesh Chugtai입니다. Gilfoyle과 경쟁하며 최고의 엔지니어임을 증명합니다.',
        )
