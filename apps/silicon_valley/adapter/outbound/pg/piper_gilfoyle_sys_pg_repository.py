from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import (
    PiperGilfoyleSysIntroduceQuery,
    PiperGilfoyleSysIntroduceResult,
)
from silicon_valley.app.ports.output.piper_gilfoyle_sys_repository import PiperGilfoyleSysRepository


class PiperGilfoyleSysPgRepository(PiperGilfoyleSysRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(
        self, query: PiperGilfoyleSysIntroduceQuery
    ) -> PiperGilfoyleSysIntroduceResult:
        return PiperGilfoyleSysIntroduceResult(
            id=query.id,
            name=query.name,
            message='시스템 엔지니어 Bertram Gilfoyle입니다. 리눅스와 보안에 통달했으며, 서버는 항상 제가 직접 관리합니다.',
        )
