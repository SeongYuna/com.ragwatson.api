from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class TitanicPassengerORM(Base):
    __tablename__ = "titanic_passengers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    passenger_id: Mapped[str]
    survived: Mapped[str]
    pclass: Mapped[str]
    name: Mapped[str]
    gender: Mapped[int]
    age: Mapped[str]
    sib_sp: Mapped[str]
    parch: Mapped[str]
    ticket: Mapped[str]
    fare: Mapped[str]
    cabin: Mapped[str]
    embarked: Mapped[str]
