from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]
    nickname: Mapped[str]
    email: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
