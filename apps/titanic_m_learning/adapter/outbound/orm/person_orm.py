from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class PersonORM(Base):
    """PersonCommand 필드와 1:1 (모든 컬럼 str)."""

    __tablename__ = "titanic_persons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    gender: Mapped[str]
    age: Mapped[str]
    sib_sp: Mapped[str]
    parch: Mapped[str]
    survived: Mapped[str]

    booking: Mapped["BookingORM"] = relationship(
        back_populates="person",
        uselist=False,
        cascade="all, delete-orphan",
    )
