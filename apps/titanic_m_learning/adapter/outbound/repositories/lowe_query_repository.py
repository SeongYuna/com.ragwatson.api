from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.lowe_orm_mapper import person_booking_to_lowe_query
from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.lowe_dto import LoweLifeboatQueryResult
from titanic_m_learning.app.ports.output.lowe_port import LowePort
from titanic_m_learning.app.dtos.lowe_dto import LoweIntroduceQuery, LoweIntroduceResult


class LoweQueryRepository(LowePort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_lifeboats(self, *, lifeboat: str | None = None) -> LoweLifeboatQueryResult:
        stmt = (
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
            .join(PersonORM.booking)
            .where(PersonORM.survived == "1")
            .order_by(PersonORM.id)
        )
        if lifeboat is not None:
            stmt = stmt.where(BookingORM.cabin == lifeboat)
        result = await self._db.execute(stmt)
        rows = result.scalars().all()
        passengers = [
            person_booking_to_lowe_query(row, row.booking)
            for row in rows
            if row.booking is not None
        ]
        return LoweLifeboatQueryResult(passengers=passengers)
    async def introduce_myself(self, query: LoweIntroduceQuery) -> LoweIntroduceResult:
        return LoweIntroduceResult(
            id=query.id,
            name=query.name,
            message='5부 Officer Harold Lowe입니다. 구명보트·생존자 기록을 조회합니다.',
        )

