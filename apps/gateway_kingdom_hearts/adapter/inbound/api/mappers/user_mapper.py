from gateway_kingdom_hearts.adapter.inbound.api.schemas.user_request import SignupRequest
from gateway_kingdom_hearts.adapter.inbound.api.schemas.user_response import (
    SignupResponse,
    SignupResponseData,
)
from gateway_kingdom_hearts.app.dto.signup_result import SignupResult
from gateway_kingdom_hearts.domain.entities.user import User


def signup_request_to_user(req: SignupRequest) -> User:
    return User.create(
        id=req.id,
        password=req.password,
        nickname=req.nickname,
        email=req.email,
        role=req.role,
    )


def signup_result_to_response(result: SignupResult) -> SignupResponse:
    return SignupResponse(
        ok=True,
        data=SignupResponseData(
            id=result.id,
            password=result.password,
            nickname=result.nickname,
            email=result.email,
            role=result.role,
        ),
    )
