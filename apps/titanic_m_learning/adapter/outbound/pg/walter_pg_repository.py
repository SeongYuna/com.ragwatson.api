from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from titanic_m_learning.adapter.outbound.mappers.walter_orm_mapper import (
    person_booking_to_query,
)
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.walter_dto import WalterPassengerQuery
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository


class WalterPgRepository(WalterRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_all(self) -> list[WalterPassengerQuery]:
        result = await self._db.execute(
            select(PersonORM)
            .options(selectinload(PersonORM.booking))
            .order_by(PersonORM.id)
        )
        rows = result.scalars().all()
        return [
            person_booking_to_query(row, row.booking)
            for row in rows
            if row.booking is not None
        ]
