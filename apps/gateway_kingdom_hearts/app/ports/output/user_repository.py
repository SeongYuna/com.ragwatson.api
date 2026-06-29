from abc import ABC, abstractmethod

from gateway_kingdom_hearts.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        """도메인 사용자를 저장소에 저장한다."""
        ...
