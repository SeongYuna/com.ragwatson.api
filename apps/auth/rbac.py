"""Permission·role→permission 매핑. Role 타입 자체는 core.security가 단일 정의처다.

core/dependencies.py의 RoleChecker와 비즈니스 앱이 core.dependencies를 통해서만
Role을 쓰도록, Role은 여기서 새로 정의하지 않고 core.security에서 가져온다.
"""

from __future__ import annotations

from enum import StrEnum

from core.security import Role

__all__ = ["Role", "Permission", "permissions_for"]


class Permission(StrEnum):
    VIEW_PROFILE = "view_profile"
    MANAGE_USERS = "manage_users"


_ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.USER: frozenset({Permission.VIEW_PROFILE}),
    Role.ADMIN: frozenset({Permission.VIEW_PROFILE, Permission.MANAGE_USERS}),
}


def permissions_for(role: Role) -> frozenset[Permission]:
    return _ROLE_PERMISSIONS.get(role, frozenset())
