"""JWT(RS256) 발급·검증, 비밀번호 해싱, JWKS — 공유 커널.

발급 함수는 호출 시점에 JWT_PRIVATE_KEY를 읽는다(모듈 로드 시 읽지 않음).
비즈니스 컨테이너에는 공개키만 있으므로, 이 모듈을 import하는 것만으로는
개인키 부재 에러가 나지 않는다.
"""

from __future__ import annotations

import base64
import json
import os
import time
import uuid
from dataclasses import dataclass
from enum import StrEnum

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

_ALGORITHM = "RS256"
_JWT_KID = os.getenv("JWT_KID", "auth-key-1")

_ph = PasswordHasher()


class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"


@dataclass(frozen=True)
class TokenPayload:
    sub: str
    roles: list[str]
    aud: str
    exp: int
    iat: int
    jti: str


class InvalidTokenError(Exception):
    """만료·서명불일치·잘못된 aud 등 검증 실패를 하나로 통일한 예외."""


COOKIE_KWARGS = dict(
    domain=".seongyuna.cloud",
    secure=True,
    httponly=True,
    samesite="lax",
)


def _read_pem_env(name: str) -> str:
    raw = os.environ[name].strip()
    if raw.startswith("-----BEGIN"):
        return raw.replace("\\n", "\n")
    return base64.b64decode(raw).decode("utf-8")


def create_access_token(
    sub: str,
    roles: list[str],
    aud: str,
    expires_min: int = 10,
) -> tuple[str, str]:
    """(token, jti)를 반환한다. jti는 로그아웃 시 블랙리스트 등록에 쓰인다."""
    private_key = _read_pem_env("JWT_PRIVATE_KEY")
    now = int(time.time())
    jti = str(uuid.uuid4())
    payload = {
        "sub": sub,
        "roles": roles,
        "aud": aud,
        "iat": now,
        "exp": now + expires_min * 60,
        "jti": jti,
    }
    token = jwt.encode(payload, private_key, algorithm=_ALGORITHM, headers={"kid": _JWT_KID})
    return token, jti


def create_refresh_token(
    sub: str,
    family_id: str | None = None,
    expires_days: int = 14,
) -> tuple[str, str, str]:
    """(token, jti, family_id)를 반환한다. family_id는 로테이션·재사용 감지 단위."""
    private_key = _read_pem_env("JWT_PRIVATE_KEY")
    now = int(time.time())
    jti = str(uuid.uuid4())
    fam = family_id or str(uuid.uuid4())
    payload = {
        "sub": sub,
        "aud": "auth",
        "type": "refresh",
        "fam": fam,
        "iat": now,
        "exp": now + expires_days * 86400,
        "jti": jti,
    }
    token = jwt.encode(payload, private_key, algorithm=_ALGORITHM, headers={"kid": _JWT_KID})
    return token, jti, fam


def verify_token(token: str, aud: str) -> TokenPayload:
    public_key = _read_pem_env("JWT_PUBLIC_KEY")
    try:
        claims = jwt.decode(token, public_key, algorithms=[_ALGORITHM], audience=aud)
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(str(exc)) from exc
    return TokenPayload(
        sub=claims["sub"],
        roles=claims.get("roles", []),
        aud=claims["aud"],
        exp=claims["exp"],
        iat=claims["iat"],
        jti=claims["jti"],
    )


def decode_refresh_token(token: str) -> dict:
    """리프레시 토큰(aud="auth")을 검증하고 원본 클레임(fam 포함)을 반환한다."""
    public_key = _read_pem_env("JWT_PUBLIC_KEY")
    try:
        return jwt.decode(token, public_key, algorithms=[_ALGORITHM], audience="auth")
    except jwt.PyJWTError as exc:
        raise InvalidTokenError(str(exc)) from exc


def hash_password(raw: str) -> str:
    return _ph.hash(raw)


def verify_password(raw: str, hashed: str) -> bool:
    try:
        return _ph.verify(hashed, raw)
    except VerifyMismatchError:
        return False


def build_jwks() -> dict:
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from jwt.algorithms import RSAAlgorithm

    public_key = load_pem_public_key(_read_pem_env("JWT_PUBLIC_KEY").encode("utf-8"))
    jwk = json.loads(RSAAlgorithm.to_jwk(public_key))
    jwk.update({"kid": _JWT_KID, "use": "sig", "alg": _ALGORITHM})
    return {"keys": [jwk]}
