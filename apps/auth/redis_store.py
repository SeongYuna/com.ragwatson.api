"""리프레시 토큰 로테이션·재사용 감지, 액세스 토큰 블랙리스트.

apps/starcraft_hub/dependencies/redis_client.py 와 동일한 패턴(모듈 레벨 싱글턴 클라이언트)을 쓴다.
키는 core/dependencies.py의 블랙리스트 조회(`auth:blacklist:{jti}`)와 접두어를 맞춘다.
"""

from __future__ import annotations

import os

from redis.asyncio import Redis, from_url

_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
_redis_client: Redis = from_url(_REDIS_URL, decode_responses=True)


def _family_key(family_id: str) -> str:
    return f"auth:refresh:family:{family_id}"


async def store_refresh_session(*, sub: str, jti: str, family_id: str, ttl_seconds: int) -> None:
    await _redis_client.set(_family_key(family_id), f"{sub}:{jti}", ex=ttl_seconds)


async def rotate_or_detect_reuse(*, family_id: str, presented_jti: str) -> str | None:
    """유효한 최신 리프레시 토큰이면 sub를 반환한다.

    이미 로테이션되어 폐기된 jti가 다시 들어오면(재사용) 세션 전체를 폐기하고 None을 반환한다.
    """
    current = await _redis_client.get(_family_key(family_id))
    if current is None:
        return None
    sub, active_jti = current.split(":", 1)
    if active_jti != presented_jti:
        await _redis_client.delete(_family_key(family_id))
        return None
    return sub


async def revoke_family(family_id: str) -> None:
    await _redis_client.delete(_family_key(family_id))


async def blacklist_access_token(*, jti: str, ttl_seconds: int) -> None:
    if ttl_seconds <= 0:
        return
    await _redis_client.set(f"auth:blacklist:{jti}", "1", ex=ttl_seconds)
