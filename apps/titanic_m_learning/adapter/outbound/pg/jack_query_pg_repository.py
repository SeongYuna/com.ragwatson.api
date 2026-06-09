from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.jack_orm_mapper import person_booking_to_jack_query
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.jack_dto import JackPassengerQuery
from titanic_m_learning.app.ports.output.jack_repository import JackRepository
from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult


class JackQueryPgRepository(JackRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        stmt = (
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
            .where(PersonORM.passenger_id == passenger_id)
        )
        result = await self._db.execute(stmt)
        person = result.scalar_one_or_none()
        if person is None or person.booking is None:
            raise LookupError(f"passenger_id={passenger_id} not found")
        return person_booking_to_jack_query(person, person.booking)
    async def introduce_myself(self, query: JackIntroduceQuery) -> JackIntroduceResult:
        return JackIntroduceResult(
            id=query.id,
            name=query.name,
            message='3등석 승객 Jack Dawson입니다.',
        )

