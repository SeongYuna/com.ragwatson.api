from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult
from titanic_machine_learning.app.ports.output.molly_port import MollyPort


class MollyQueryRepository(MollyPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        return MollyIntroduceResult(
            id=query.id,
            name=query.name,
            message='Molly Brown입니다.',
        )
