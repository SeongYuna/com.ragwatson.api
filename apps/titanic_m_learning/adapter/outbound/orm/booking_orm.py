from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM


class BookingORM(Base):
    """BookingCommand(james_cmd_dto) + person.passenger_id FK. 모든 값 컬럼은 str."""

    __tablename__ = "titanic_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("titanic_persons.passenger_id"),
        unique=True,
        index=True,
        nullable=False,
    )
    pclass: Mapped[str] = mapped_column(String, nullable=False)
    ticket: Mapped[str] = mapped_column(String, nullable=False)
    fare: Mapped[str] = mapped_column(String, nullable=False)
    cabin: Mapped[str] = mapped_column(String, nullable=False)
    embarked: Mapped[str] = mapped_column(String, nullable=False)

    person: Mapped[PersonORM] = relationship(back_populates="booking")
