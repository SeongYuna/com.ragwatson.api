"""GET /login/{provider}(인가 시작), GET /callback/{provider}, POST /refresh, POST /logout,
GET /.well-known/jwks.json.

POST /login(아이디/비번)은 이번 범위 밖 — AuthAccount는 OAuth 전용이라 비밀번호 필드가 없다
(harness 문서 "회원가입 등은 이번 범위 밖" 방침을 로컬 로그인까지 확장 적용).
"""

from __future__ import annotations

import secrets
import time

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from auth import redis_store, repository, services
from auth.schemas import LogoutRequest, RefreshRequest, TokenResponse
from core.database import get_db
from core.security import (
    COOKIE_KWARGS,
    InvalidTokenError,
    build_jwks,
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    verify_token,
)

router = APIRouter(tags=["auth"])

_STATE_COOKIE = "oauth_state"


@router.get("/login/{provider}")
async def login(provider: str) -> RedirectResponse:
    if not services.is_supported_provider(provider):
        raise HTTPException(status_code=404, detail="지원하지 않는 provider입니다.")

    state = secrets.token_hex(16)
    authorize_url = services.build_authorize_url(provider, services.get_redirect_uri(provider), state)

    response = RedirectResponse(authorize_url, status_code=302)
    response.set_cookie(
        _STATE_COOKIE,
        state,
        max_age=600,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )
    return response


@router.get("/callback/{provider}")
async def callback(
    provider: str,
    request: Request,
    code: str | None = None,
    state: str | None = None,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    def failure(reason: str) -> RedirectResponse:
        url = f"{services.FRONTEND_URL}/?auth=error&provider={provider}&reason={reason}"
        return RedirectResponse(url, status_code=302)

    if not services.is_supported_provider(provider):
        return failure("unsupported_provider")

    saved_state = request.cookies.get(_STATE_COOKIE)
    if not code or not state or not saved_state or state != saved_state:
        return failure("invalid_state")

    try:
        profile = await services.exchange_code_for_profile(
            provider, code, services.get_redirect_uri(provider)
        )
    except (httpx.HTTPError, ValueError, KeyError):
        return failure("token_exchange_failed")

    access_token, refresh_token = await services.issue_session_for_profile(db, profile)

    response = RedirectResponse(
        f"{services.FRONTEND_URL}/?auth=success&provider={provider}", status_code=302
    )
    response.delete_cookie(_STATE_COOKIE, path="/")
    response.set_cookie(
        "access_token", access_token, max_age=services.ACCESS_TOKEN_EXPIRES_MIN * 60, **COOKIE_KWARGS
    )
    response.set_cookie(
        "refresh_token", refresh_token, max_age=services.REFRESH_TOKEN_EXPIRES_DAYS * 86400, **COOKIE_KWARGS
    )
    return response


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    request: Request,
    response: Response,
    body: RefreshRequest | None = None,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    token = (body.refresh_token if body else None) or request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="refresh_token이 없습니다.")

    try:
        claims = decode_refresh_token(token)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="유효하지 않은 refresh_token입니다.") from exc

    family_id = claims["fam"]
    sub = await redis_store.rotate_or_detect_reuse(family_id=family_id, presented_jti=claims["jti"])
    if sub is None:
        raise HTTPException(
            status_code=401, detail="재사용이 감지되어 세션이 폐기되었습니다. 다시 로그인하세요."
        )

    account = await repository.get_by_id(db, sub)
    roles = [account.role] if account else []
    access_token, _access_jti = create_access_token(
        sub=sub, roles=roles, aud=services.SERVICE_AUD, expires_min=services.ACCESS_TOKEN_EXPIRES_MIN
    )
    new_refresh_token, new_jti, _fam = create_refresh_token(
        sub=sub, family_id=family_id, expires_days=services.REFRESH_TOKEN_EXPIRES_DAYS
    )
    await redis_store.store_refresh_session(
        sub=sub,
        jti=new_jti,
        family_id=family_id,
        ttl_seconds=services.REFRESH_TOKEN_EXPIRES_DAYS * 86400,
    )
    response.set_cookie(
        "access_token", access_token, max_age=services.ACCESS_TOKEN_EXPIRES_MIN * 60, **COOKIE_KWARGS
    )
    response.set_cookie(
        "refresh_token",
        new_refresh_token,
        max_age=services.REFRESH_TOKEN_EXPIRES_DAYS * 86400,
        **COOKIE_KWARGS,
    )
    return TokenResponse(access_token=access_token)


@router.post("/logout")
async def logout(request: Request, response: Response, body: LogoutRequest | None = None) -> dict:
    token = (body.refresh_token if body else None) or request.cookies.get("refresh_token")
    if token:
        try:
            claims = decode_refresh_token(token)
            await redis_store.revoke_family(claims["fam"])
        except InvalidTokenError:
            pass

    access_token = request.cookies.get("access_token")
    if access_token:
        try:
            payload = verify_token(access_token, aud=services.SERVICE_AUD)
        except InvalidTokenError:
            pass
        else:
            ttl = max(payload.exp - int(time.time()), 0)
            await redis_store.blacklist_access_token(jti=payload.jti, ttl_seconds=ttl)

    response.delete_cookie("access_token", domain=COOKIE_KWARGS["domain"], path="/")
    response.delete_cookie("refresh_token", domain=COOKIE_KWARGS["domain"], path="/")
    return {"ok": True}


@router.get("/.well-known/jwks.json")
async def jwks() -> dict:
    return build_jwks()
