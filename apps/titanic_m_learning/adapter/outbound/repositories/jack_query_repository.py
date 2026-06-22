from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.jack_orm_mapper import person_booking_to_jack_query
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult, JackPassengerQuery, JackTrainRow
from titanic_m_learning.app.ports.output.jack_port import JackPort


class JackQueryRepository(JackPort):
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

    async def fetch_all_for_training(self) -> list[JackTrainRow]:
        stmt = (
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
        )
        result = await self._db.execute(stmt)
        persons = result.scalars().all()
        return [
            JackTrainRow(
                passenger_id=p.passenger_id,
                name=p.name,
                gender=p.gender,
                survived=p.survived,
                pclass=p.booking.pclass,
                age=p.age,
                sib_sp=p.sib_sp,
                parch=p.parch,
                ticket=p.booking.ticket,
                fare=p.booking.fare,
                cabin=p.booking.cabin,
                embarked=p.booking.embarked,
            )
            for p in persons
            if p.booking is not None
        ]