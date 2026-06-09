from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.molly_orm_mapper import person_booking_to_molly_query
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.molly_dto import MollyNotableQueryResult
from titanic_m_learning.app.ports.output.molly_repository import MollyRepository
from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult


class MollyQueryPgRepository(MollyRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_notable(self) -> MollyNotableQueryResult:
        stmt = (
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
            .where(
                PersonORM.survived == "1",
                PersonORM.gender == "female",
            )
            .order_by(PersonORM.id)
        )
        result = await self._db.execute(stmt)
        rows = result.scalars().all()
        passengers = [
            person_booking_to_molly_query(row, row.booking)
            for row in rows
            if row.booking is not None
        ]
        return MollyNotableQueryResult(passengers=passengers)
    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        return MollyIntroduceResult(
            id=query.id,
            name=query.name,
            message='Molly Brown입니다. 주목할 만한 여성 생존자 기록을 조회합니다.',
        )

