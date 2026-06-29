from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult
from titanic_machine_learning.app.ports.output.isador_port import IsadorPort


class IsadorQueryRepository(IsadorPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        return IsadorIntroduceResult(
            id=query.id,
            name=query.name,
            message='Isidor Straus입니다.',
        )
