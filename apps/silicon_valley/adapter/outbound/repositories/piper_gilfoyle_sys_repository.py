from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import (
    PiperGilfoyleSysIntroduceQuery,
    PiperGilfoyleSysIntroduceResult,
)
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import PiperGilfoyleSysRepository


class PiperGilfoyleSysQueryRepository(PiperGilfoyleSysRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(
        self, query: PiperGilfoyleSysIntroduceQuery
    ) -> PiperGilfoyleSysIntroduceResult:
        return PiperGilfoyleSysIntroduceResult(
            id=query.id,
            name=query.name,
            message="나는 시스템 엔지니어 버트럼 길포일입니다.",
        )
