"""OAuth Provider 연동(Google/Kakao/Naver), 토큰 발급 오케스트레이션.

인가 URL 구성 → 콜백에서 code를 프로필로 교환 → AuthAccount 조회/생성 →
access/refresh 토큰 발급까지 이 모듈이 전 과정을 처리한다(harness 문서 방침).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Callable
from urllib.parse import urlencode

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from auth import redis_store
from auth.models import AuthAccountORM
from auth.repository import get_or_create_by_provider
from core.security import create_access_token, create_refresh_token

SERVICE_AUD = os.getenv("SERVICE_AUD", "seongyuna-api")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://seongyuna.cloud")
ACCESS_TOKEN_EXPIRES_MIN = 10
REFRESH_TOKEN_EXPIRES_DAYS = 14


@dataclass(frozen=True)
class OAuthProfile:
    provider: str
    provider_user_id: str
    email: str | None
    nickname: str | None


@dataclass(frozen=True)
class ProviderConfig:
    authorize_url: str
    token_url: str
    profile_url: str
    client_id_env: str
    client_secret_env: str
    redirect_uri_env: str
    scope: str | None
    parse_profile: Callable[[dict[str, Any]], OAuthProfile]


def _parse_google(raw: dict[str, Any]) -> OAuthProfile:
    return OAuthProfile(
        provider="google",
        provider_user_id=str(raw.get("sub", "")),
        email=raw.get("email"),
        nickname=raw.get("name"),
    )


def _parse_kakao(raw: dict[str, Any]) -> OAuthProfile:
    account = raw.get("kakao_account") or {}
    return OAuthProfile(
        provider="kakao",
        provider_user_id=str(raw.get("id", "")),
        email=account.get("email"),
        nickname=(account.get("profile") or {}).get("nickname"),
    )


def _parse_naver(raw: dict[str, Any]) -> OAuthProfile:
    response = raw.get("response") or {}
    return OAuthProfile(
        provider="naver",
        provider_user_id=str(response.get("id", "")),
        email=response.get("email"),
        nickname=response.get("name"),
    )


PROVIDERS: dict[str, ProviderConfig] = {
    "google": ProviderConfig(
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        token_url="https://oauth2.googleapis.com/token",
        profile_url="https://www.googleapis.com/oauth2/v3/userinfo",
        client_id_env="GOOGLE_CLIENT_ID",
        client_secret_env="GOOGLE_CLIENT_SECRET",
        redirect_uri_env="GOOGLE_REDIRECT_URI",
        scope="openid email profile",
        parse_profile=_parse_google,
    ),
    "kakao": ProviderConfig(
        authorize_url="https://kauth.kakao.com/oauth/authorize",
        token_url="https://kauth.kakao.com/oauth/token",
        profile_url="https://kapi.kakao.com/v2/user/me",
        client_id_env="KAKAO_CLIENT_ID",
        client_secret_env="KAKAO_CLIENT_SECRET",
        redirect_uri_env="KAKAO_REDIRECT_URI",
        scope=None,
        parse_profile=_parse_kakao,
    ),
    "naver": ProviderConfig(
        authorize_url="https://nid.naver.com/oauth2.0/authorize",
        token_url="https://nid.naver.com/oauth2.0/token",
        profile_url="https://openapi.naver.com/v1/nid/me",
        client_id_env="NAVER_CLIENT_ID",
        client_secret_env="NAVER_CLIENT_SECRET",
        redirect_uri_env="NAVER_REDIRECT_URI",
        scope=None,
        parse_profile=_parse_naver,
    ),
}


def is_supported_provider(provider: str) -> bool:
    return provider in PROVIDERS


def get_redirect_uri(provider: str) -> str:
    """provider별 *_REDIRECT_URI env(.env.auth)를 그대로 쓴다 — OAuth 콘솔에 등록된 값과 반드시 일치해야 한다."""
    return os.environ[PROVIDERS[provider].redirect_uri_env]


def build_authorize_url(provider: str, redirect_uri: str, state: str) -> str:
    config = PROVIDERS[provider]
    client_id = os.environ[config.client_id_env]
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "state": state,
    }
    if config.scope:
        params["scope"] = config.scope
    return f"{config.authorize_url}?{urlencode(params)}"


async def exchange_code_for_profile(provider: str, code: str, redirect_uri: str) -> OAuthProfile:
    config = PROVIDERS[provider]
    client_id = os.environ[config.client_id_env]
    client_secret = os.environ[config.client_secret_env]

    async with httpx.AsyncClient(timeout=10.0) as client:
        token_res = await client.post(
            config.token_url,
            headers={"Accept": "application/json"},
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
        )
        token_res.raise_for_status()
        access_token = token_res.json().get("access_token")
        if not access_token:
            raise ValueError("token_exchange_failed")

        profile_res = await client.get(
            config.profile_url,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_res.raise_for_status()
        return config.parse_profile(profile_res.json())


async def issue_session_for_profile(db: AsyncSession, profile: OAuthProfile) -> tuple[str, str]:
    """(access_token, refresh_token)을 반환한다. 신규면 AuthAccount를 생성한다."""
    account: AuthAccountORM = await get_or_create_by_provider(
        db,
        provider=profile.provider,
        provider_user_id=profile.provider_user_id,
        email=profile.email,
        nickname=profile.nickname,
    )

    access_token, _access_jti = create_access_token(
        sub=account.id,
        roles=[account.role],
        aud=SERVICE_AUD,
        expires_min=ACCESS_TOKEN_EXPIRES_MIN,
    )
    refresh_token, refresh_jti, family_id = create_refresh_token(
        sub=account.id,
        expires_days=REFRESH_TOKEN_EXPIRES_DAYS,
    )
    await redis_store.store_refresh_session(
        sub=account.id,
        jti=refresh_jti,
        family_id=family_id,
        ttl_seconds=REFRESH_TOKEN_EXPIRES_DAYS * 86400,
    )
    return access_token, refresh_token
