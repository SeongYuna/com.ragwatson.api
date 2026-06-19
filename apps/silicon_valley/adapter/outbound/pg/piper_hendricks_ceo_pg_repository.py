from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    PiperHendricksCeoIntroduceQuery,
    PiperHendricksCeoIntroduceResult,
)
from silicon_valley.app.ports.output.piper_hendricks_ceo_repository import PiperHendricksCeoRepository


class PiperHendricksCeoPgRepository(PiperHendricksCeoRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(
        self, query: PiperHendricksCeoIntroduceQuery
    ) -> PiperHendricksCeoIntroduceResult:
        return PiperHendricksCeoIntroduceResult(
            id=query.id,
            name=query.name,
            message='파이드 파이퍼 CEO Richard Hendricks입니다. 중간 아웃(Middle-Out) 압축 알고리즘을 발명했습니다.',
        )
