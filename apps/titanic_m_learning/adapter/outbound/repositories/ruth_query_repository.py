from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.app.dtos.ruth_dto import RuthIntroduceQuery, RuthIntroduceResult
from titanic_m_learning.app.ports.output.ruth_port import RuthPort


class RuthQueryRepository(RuthPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        return RuthIntroduceResult(
            id=query.id,
            name=query.name,
            message='Ruth입니다.',
        )
