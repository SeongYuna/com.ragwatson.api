"""인증된 사용자 조회 + 역할 검사 — 공유 커널.

비즈니스 앱은 이 모듈만 import한다(apps.auth를 직접 import하지 않는다).
core는 apps.auth를 전혀 import하지 않으므로 의존 방향은 항상 앱→core로 유지된다.
"""

from __future__ import annotations

import os

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis, from_url

from core.security import InvalidTokenError, Role, TokenPayload, verify_token

_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_redis_client: Redis = from_url(_REDIS_URL, decode_responses=True)


def _extract_token(request: Request) -> str | None:
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        return cookie_token
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.removeprefix("Bearer ").strip()
    return None


async def get_current_user(request: Request) -> TokenPayload:
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증이 필요합니다.")

    service_aud = os.getenv("SERVICE_AUD", "").strip()
    if not service_aud:
        raise RuntimeError("SERVICE_AUD 환경변수가 설정되지 않았습니다.")

    try:
        payload = verify_token(token, aud=service_aud)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다."
        ) from exc

    if await _redis_client.exists(f"auth:blacklist:{payload.jti}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="폐기된 토큰입니다.")

    return payload


class RoleChecker:
    def __init__(self, *allowed: Role) -> None:
        self._allowed = set(allowed)

    def __call__(self, user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if not self._allowed.intersection(user.roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다.")
        return user
