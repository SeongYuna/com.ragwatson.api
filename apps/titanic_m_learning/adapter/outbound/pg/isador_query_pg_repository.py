from sqlalchemy import Select, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.isador_orm_mapper import person_booking_to_isador_query
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.isador_dto import IsadorPassengerQuery
from titanic_m_learning.app.ports.output.isador_repository import IsadorRepository
from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery, IsadorIntroduceResult


def _person_with_booking_select() -> Select:
    return select(PersonORM).options(selectinload(PersonORM.booking))


async def _fetch_isador_queries(db: AsyncSession, stmt: Select) -> list[IsadorPassengerQuery]:
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        person_booking_to_isador_query(row, row.booking)
        for row in rows
        if row.booking is not None
    ]


class IsadorQueryPgRepository(IsadorRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_families(self) -> list[IsadorPassengerQuery]:
        stmt = (
            _person_with_booking_select()
            .where(
                or_(
                    PersonORM.sib_sp != "0",
                    PersonORM.parch != "0",
                )
            )
            .order_by(PersonORM.id)
        )
        return await _fetch_isador_queries(self._db, stmt)
    async def introduce_myself(self, query: IsadorIntroduceQuery) -> IsadorIntroduceResult:
        return IsadorIntroduceResult(
            id=query.id,
            name=query.name,
            message='Isidor Straus입니다. 가족 동반 승객 기록을 조회합니다.',
        )

