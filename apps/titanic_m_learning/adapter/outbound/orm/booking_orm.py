from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class BookingORM(Base):
    """BookingCommand 필드 + person.passenger_id FK (모든 컬럼 str)."""

    __tablename__ = "titanic_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(
        ForeignKey("titanic_persons.passenger_id"),
        unique=True,
        index=True,
    )
    pclass: Mapped[str]
    ticket: Mapped[str]
    fare: Mapped[str]
    cabin: Mapped[str]
    embarked: Mapped[str]

    person: Mapped["PersonORM"] = relationship(back_populates="booking")
 