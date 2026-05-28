import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.mappers.titanic_orm_mapper import passenger_to_orm
from titanic_m_learning.app.ports.output.james_repository import JamesRepository
from titanic_m_learning.domain.entities.titanic import TitanicPassenger

log = logging.getLogger("titanic.write")


class JamesPgRepository(JamesRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save_all(self, passengers: list[TitanicPassenger]) -> None:
        orm_rows = [passenger_to_orm(p) for p in passengers]
        log.info(
            "  ⑥ Outbound Adapter │ JamesPgRepository    │ Domain → ORM   │ %d건",
            len(orm_rows),
        )
        try:
            self._db.add_all(orm_rows)
            await self._db.commit()
        except Exception:
            await self._db.rollback()
            log.error("  ✗ NeonDB INSERT 실패 — rollback")
            raise
        log.info(
            "  ⑥ Outbound Adapter │ JamesPgRepository    │ NeonDB INSERT  │ commit ✓",
        )
