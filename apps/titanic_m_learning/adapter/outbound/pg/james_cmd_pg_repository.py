from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM
from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.james_cmd_dto import (
    JamesIntroduceQuery,
    JamesIntroduceResult,
    JamesPassengerCommand,
)
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository

_BATCH_SIZE = 500
_PERSON_UPSERT_COLS = ("name", "gender", "age", "sib_sp", "parch", "survived")
_BOOKING_UPSERT_COLS = ("pclass", "ticket", "fare", "cabin", "embarked")


def _person_row(command: JamesPassengerCommand) -> dict[str, str]:
    person = command.person
    return {
        "passenger_id": person.passenger_id,
        "name": person.name,
        "gender": person.gender,
        "age": person.age,
        "sib_sp": person.sib_sp,
        "parch": person.parch,
        "survived": person.survived,
    }


def _booking_row(command: JamesPassengerCommand) -> dict[str, str]:
    booking = command.booking
    return {
        "passenger_id": command.person.passenger_id,
        "pclass": booking.pclass,
        "ticket": booking.ticket,
        "fare": booking.fare,
        "cabin": booking.cabin,
        "embarked": booking.embarked,
    }


def _upsert_batches(
    model: type[PersonORM] | type[BookingORM],
    rows: list[dict[str, str]],
    index_col: str,
    update_cols: tuple[str, ...],
) -> list:
    statements = []
    for start in range(0, len(rows), _BATCH_SIZE):
        chunk = rows[start : start + _BATCH_SIZE]
        stmt = pg_insert(model).values(chunk)
        stmt = stmt.on_conflict_do_update(
            index_elements=[index_col],
            set_={col: stmt.excluded[col] for col in update_cols},
        )
        statements.append(stmt)
    return statements


class JamesCmdPgRepository(JamesCmdRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save_all(self, commands: list[JamesPassengerCommand]) -> None:
        """passenger_id 기준 배치 UPSERT (Neon 왕복 최소화)."""
        if not commands:
            return

        person_rows = [_person_row(command) for command in commands]
        booking_rows = [_booking_row(command) for command in commands]

        try:
            for stmt in _upsert_batches(
                PersonORM,
                person_rows,
                PersonORM.passenger_id.key,
                _PERSON_UPSERT_COLS,
            ):
                await self._db.execute(stmt)

            for stmt in _upsert_batches(
                BookingORM,
                booking_rows,
                BookingORM.passenger_id.key,
                _BOOKING_UPSERT_COLS,
            ):
                await self._db.execute(stmt)

            await self._db.commit()
        except Exception:
            await self._db.rollback()
            raise

    async def introduce_myself(self, query: JamesIntroduceQuery) -> JamesIntroduceResult:
        return JamesIntroduceResult(
            id=query.id,
            name=query.name,
            message="James입니다. CSV 업로드로 승객 데이터를 DB에 적재합니다.",
        )
