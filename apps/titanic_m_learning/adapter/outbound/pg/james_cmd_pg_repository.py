from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.mappers.james_orm_mapper import (
    command_to_booking_orm,
    command_to_person_orm,
)
from titanic_m_learning.app.dtos.james_cmd_dto import JamesPassengerCommand
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository


class JamesCmdPgRepository(JamesCmdRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save_all(self, commands: list[JamesPassengerCommand]) -> None:
        persons = [command_to_person_orm(command) for command in commands]
        bookings = [command_to_booking_orm(command) for command in commands]
        try:
            self._db.add_all(persons)
            await self._db.flush()
            self._db.add_all(bookings)
            await self._db.commit()
        except Exception:
            await self._db.rollback()
            raise
