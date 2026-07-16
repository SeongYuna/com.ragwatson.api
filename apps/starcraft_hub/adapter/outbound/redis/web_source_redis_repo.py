from __future__ import annotations

from redis.asyncio import Redis

from starcraft_hub.app.ports.output.web_source_port import WebSourcePort


class WebSourceRedisRepo(WebSourcePort):
    """Redis SET `starcraft_hub:{namespace}:websites` / `:keywords`에서 소스를 읽는다.

    namespace로 crawler/scrapper 각각의 사이트·키워드 목록을 분리한다(독립 실행).
    """

    def __init__(self, redis_client: Redis, namespace: str) -> None:
        self._redis = redis_client
        self._websites_key = f"starcraft_hub:{namespace}:websites"
        self._keywords_key = f"starcraft_hub:{namespace}:keywords"

    async def get_websites(self) -> list[str]:
        members = await self._redis.smembers(self._websites_key)
        return sorted(members)

    async def get_keywords(self) -> list[str]:
        members = await self._redis.smembers(self._keywords_key)
        return sorted(members)
