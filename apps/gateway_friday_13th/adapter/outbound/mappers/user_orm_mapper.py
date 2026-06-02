from gateway_friday_13th.adapter.outbound.orm.user_orm import UserORM
from gateway_friday_13th.domain.entities.user import User


def user_to_orm(user: User) -> UserORM:
    return UserORM(
        id=user.id,
        password=user.password,
        nickname=user.nickname,
        email=user.email,
        role=user.role,
    )


def orm_to_user(row: UserORM) -> User:
    return User(
        id=row.id,
        password=row.password,
        nickname=row.nickname,
        email=row.email,
        role=row.role,
    )
