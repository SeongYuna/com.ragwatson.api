from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

if TYPE_CHECKING:
    from titanic_m_learning.adapter.outbound.orm.booking_orm import BookingORM


class PersonORM(Base):
    """PersonCommand(james_cmd_dto)와 1:1. 업무 키는 passenger_id, PK는 id."""

    __tablename__ = "titanic_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[str] = mapped_column(String, nullable=False)
    age: Mapped[str] = mapped_column(String, nullable=False)
    sib_sp: Mapped[str] = mapped_column(String, nullable=False)
    parch: Mapped[str] = mapped_column(String, nullable=False)
    survived: Mapped[str] = mapped_column(String, nullable=False)

    booking: Mapped[BookingORM | None] = relationship(
        back_populates="person",
        uselist=False,
        cascade="all, delete-orphan",
    )
