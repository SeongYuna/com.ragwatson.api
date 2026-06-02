from abc import ABC, abstractmethod

from gateway_friday_13th.app.dto.signup_result import SignupResult
from gateway_friday_13th.domain.entities.user import User


class UserCmdUseCase(ABC):
    @abstractmethod
    async def signup(self, user: User) -> SignupResult:
        """새 사용자를 등록한다."""
        ...
