from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_machine_learning.adapter.outbound.mappers.andrew_orm_mapper import person_booking_to_andrew_query
from titanic_machine_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_machine_learning.app.dtos.andrew_dto import AndrewPageQueryResult, AndrewPassengerQuery
from titanic_machine_learning.app.ports.output.andrew_port import AndrewPort
from titanic_machine_learning.app.dtos.andrew_dto import AndrewIntroduceQuery, AndrewIntroduceResult


def _person_with_booking_select() -> Select:
    return select(PersonORM).options(selectinload(PersonORM.booking))


async def _fetch_andrew_queries(db: AsyncSession, stmt: Select) -> list[AndrewPassengerQuery]:
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [
        person_booking_to_andrew_query(row, row.booking)
        for row in rows
        if row.booking is not None
    ]


async def _count_persons_with_booking(db: AsyncSession) -> int:
    total = await db.scalar(
        select(func.count())
        .select_from(PersonORM)
        .join(PersonORM.booking)
    )
    return int(total or 0)


class AndrewQueryRepository(AndrewPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_page(self, *, skip: int, limit: int) -> AndrewPageQueryResult:
        total = await _count_persons_with_booking(self._db)
        stmt = (
            _person_with_booking_select()
            .order_by(PersonORM.id)
            .offset(skip)
            .limit(limit)
        )
        passengers = await _fetch_andrew_queries(self._db, stmt)
        return AndrewPageQueryResult(
            passengers=passengers,
            skip=skip,
            limit=limit,
            total=total,
        )
    async def introduce_myself(self, query: AndrewIntroduceQuery) -> AndrewIntroduceResult:
        return AndrewIntroduceResult(
            id=query.id,
            name=query.name,
            message='저는 타이타닉의 수석 설계자 토마스 앤드류스입니다.',
        )

