from fastapi import APIRouter, Depends, HTTPException

from gateway_friday_13th.adapter.inbound.api.dependencies import get_user_cmd_use_case
from gateway_friday_13th.adapter.inbound.api.mappers.user_mapper import (
    signup_request_to_user,
    signup_result_to_response,
)
from gateway_friday_13th.adapter.inbound.api.schemas.user_request import SignupRequest
from gateway_friday_13th.adapter.inbound.api.schemas.user_response import SignupResponse
from gateway_friday_13th.app.ports.input.user_cmd_use_case import UserCmdUseCase

user_cmd_router = APIRouter(tags=["gateway"])


@user_cmd_router.post("/signup", response_model=SignupResponse)
async def signup(
    body: SignupRequest,
    use_case: UserCmdUseCase = Depends(get_user_cmd_use_case),
) -> SignupResponse:
    try:
        result = await use_case.signup(signup_request_to_user(body))
    except ValueError as exc:
        msg = str(exc)
        if msg == "duplicate":
            raise HTTPException(
                status_code=409,
                detail="이미 존재하는 아이디 또는 이메일입니다.",
            ) from exc
        if msg == "schema":
            raise HTTPException(
                status_code=500,
                detail="DB 테이블 스키마가 맞지 않습니다. 서버를 재시작해 주세요.",
            ) from exc
        raise HTTPException(status_code=500, detail=msg) from exc
    return signup_result_to_response(result)
