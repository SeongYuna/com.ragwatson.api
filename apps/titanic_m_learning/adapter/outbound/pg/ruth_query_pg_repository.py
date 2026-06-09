from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.ruth_orm_mapper import person_booking_to_ruth_query
from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.ruth_dto import RuthPassengerQuery
from titanic_m_learning.app.ports.output.ruth_repository import RuthRepository
from titanic_m_learning.app.dtos.ruth_dto import RuthIntroduceQuery, RuthIntroduceResult


def _person_with_booking_select() -> Select:
    return select(PersonORM).options(selectinload(PersonORM.booking))


async def _fetch_ruth_queries(db: AsyncSession, stmt: Select) -> list[RuthPassengerQuery]:
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        person_booking_to_ruth_query(row, row.booking)
        for row in rows
        if row.booking is not None
    ]


class RuthQueryPgRepository(RuthRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_first_class(self) -> list[RuthPassengerQuery]:
        stmt = (
            _person_with_booking_select()
            .join(PersonORM.booking)
            .where(BookingORM.pclass == "1")
            .order_by(PersonORM.id)
        )
        return await _fetch_ruth_queries(self._db, stmt)
    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        return RuthIntroduceResult(
            id=query.id,
            name=query.name,
            message='Ruth입니다. 1등석 승객 목록을 조회합니다.',
        )

