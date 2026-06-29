from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_machine_learning.adapter.outbound.mappers.walter_orm_mapper import person_booking_to_walter_query
from titanic_machine_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_machine_learning.app.dtos.walter_dto import WalterPassengerQuery
from titanic_machine_learning.app.ports.output.walter_port import WalterPort
from titanic_machine_learning.app.dtos.walter_dto import WalterIntroduceQuery, WalterIntroduceResult


class WalterRepository(WalterPort):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_all(self) -> list[WalterPassengerQuery]:
        stmt = (
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
            .order_by(PersonORM.id)
        )
        result = await self._db.execute(stmt)
        rows = result.scalars().all()
        return [
            person_booking_to_walter_query(row, row.booking)
            for row in rows
            if row.booking is not None
        ]
    async def introduce_myself(self, query: WalterIntroduceQuery) -> WalterIntroduceResult:
        return WalterIntroduceResult(
            id=query.id,
            name=query.name,
            message='저는 Walter입니다. 타이타닉 승객 전체 기록을 조회합니다.',
        )

    async def get_train_set(self) -> list[WalterPassengerQuery]:
        all_passengers = await self.find_all()
        split = int(len(all_passengers) * 0.8)
        return all_passengers[:split]

    async def get_test_set(self) -> list[WalterPassengerQuery]:
        all_passengers = await self.find_all()
        split = int(len(all_passengers) * 0.8)
        return all_passengers[split:]

