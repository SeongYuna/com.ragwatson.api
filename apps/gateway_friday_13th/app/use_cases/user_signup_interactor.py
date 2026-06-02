from gateway_friday_13th.app.dto.signup_result import SignupResult
from gateway_friday_13th.app.ports.input.user_cmd_use_case import UserCmdUseCase
from gateway_friday_13th.app.ports.output.user_repository import UserRepository
from gateway_friday_13th.domain.entities.user import User


class UserSignupInteractor(UserCmdUseCase):
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    async def signup(self, user: User) -> SignupResult:
        await self._repository.save(user)
        return SignupResult(
            id=user.id,
            password=user.password,
            nickname=user.nickname,
            email=user.email,
            role=user.role,
        )
