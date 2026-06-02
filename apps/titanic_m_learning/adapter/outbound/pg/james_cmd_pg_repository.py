import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.mappers.titanic_orm_mapper import command_to_orm
from titanic_m_learning.app.dtos.james_cmd_dto import JamesPassengerCommand
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository

log = logging.getLogger("titanic.write")


class JamesCmdPgRepository(JamesCmdRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save_all(self, commands: list[JamesPassengerCommand]) -> None:
        orm_rows = [command_to_orm(command) for command in commands]
        log.info(
            "  ⑥ Outbound Adapter │ JamesCmdPgRepository    │ Command → ORM  │ %d건",
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
            "  ⑥ Outbound Adapter │ JamesCmdPgRepository    │ NeonDB INSERT  │ commit ✓",
        )
