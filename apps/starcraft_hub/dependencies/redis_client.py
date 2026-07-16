from __future__ import annotations

import os

from redis.asyncio import Redis, from_url

_REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

_redis_client: Redis = from_url(_REDIS_URL, decode_responses=True)


def get_redis_client() -> Redis:
    return _redis_client
