from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.hartley_orm_mapper import person_booking_to_hartley_query
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.hartley_dto import HartleyPassengerQuery
from titanic_m_learning.app.ports.output.hartley_repository import HartleyRepository
from titanic_m_learning.app.dtos.hartley_dto import HartleyIntroduceQuery, HartleyIntroduceResult


def _person_with_booking_select() -> Select:
    return select(PersonORM).options(selectinload(PersonORM.booking))


async def _fetch_hartley_queries(db: AsyncSession, stmt: Select) -> list[HartleyPassengerQuery]:
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        person_booking_to_hartley_query(row, row.booking)
        for row in rows
        if row.booking is not None
    ]


class HartleyQueryPgRepository(HartleyRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def sample(self, *, count: int) -> list[HartleyPassengerQuery]:
        stmt = (
            _person_with_booking_select()
            .order_by(func.random())
            .limit(count)
        )
        return await _fetch_hartley_queries(self._db, stmt)
    async def introduce_myself(self, query: HartleyIntroduceQuery) -> HartleyIntroduceResult:
        return HartleyIntroduceResult(
            id=query.id,
            name=query.name,
            message='타이타닉 밴드마스터 Wallace Hartley입니다.',
        )

