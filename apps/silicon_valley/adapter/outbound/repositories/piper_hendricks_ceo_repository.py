from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    PiperHendricksCeoIntroduceQuery,
    PiperHendricksCeoIntroduceResult,
)
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import PiperHendricksCeoRepository


class PiperHendricksCeoQueryRepository(PiperHendricksCeoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def introduce_myself(
        self, query: PiperHendricksCeoIntroduceQuery
    ) -> PiperHendricksCeoIntroduceResult:
        return PiperHendricksCeoIntroduceResult(
            id=query.id,
            name=query.name,
            message="안녕하세요, Pied Piper CEO 리처드 헨드릭스입니다.",
        )
