import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.mappers.titanic_orm_mapper import orm_to_passenger
from titanic_m_learning.adapter.outbound.orm.titanic_orm import TitanicPassengerORM
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository
from titanic_m_learning.domain.entities.titanic import TitanicPassenger

log = logging.getLogger("titanic.read")


class WalterPgRepository(WalterRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def find_all(self) -> list[TitanicPassenger]:
        log.info(
            "  ⑤ Outbound Adapter │ WalterPgRepository   │ NeonDB SELECT",
        )
        result = await self._db.execute(
            select(TitanicPassengerORM).order_by(TitanicPassengerORM.id)
        )
        rows = result.scalars().all()
        passengers = [orm_to_passenger(row) for row in rows]
        log.info(
            "  ⑤ Outbound Adapter │ WalterPgRepository   │ ORM → Domain   │ %d건",
            len(passengers),
        )
        return passengers
