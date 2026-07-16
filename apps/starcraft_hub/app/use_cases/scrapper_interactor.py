from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from starcraft_hub.app.dtos.scrapper_dto import ScrapeResult
from starcraft_hub.app.ports.input.scrapper_port import ScrapperPort
from starcraft_hub.app.ports.output.result_storage_port import ResultStoragePort
from starcraft_hub.app.ports.output.web_source_port import WebSourcePort

_TIMEOUT_SECONDS = 10.0
_USER_AGENT = "StarcraftHubScrapper/1.0"
_TARGET_TAGS = ["p", "li", "h1", "h2", "h3"]


class ScrapperInteractor(ScrapperPort):
    """Redis에 등록된 웹사이트 1페이지씩만 방문해 키워드가 포함된 문단을 추출한다.

    크롤러와 달리 링크를 따라가지 않는다(독립 실행, 시드 URL 단건 대상).
    """

    def __init__(self, web_source: WebSourcePort, storage: ResultStoragePort) -> None:
        self._web_source = web_source
        self._storage = storage

    async def scrape(
        self,
        websites: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> ScrapeResult:
        if websites is None:
            websites = await self._web_source.get_websites()
        if keywords is None:
            keywords = await self._web_source.get_keywords()

        saved_files: list[str] = []
        items_extracted = 0
        async with httpx.AsyncClient(
            headers={"User-Agent": _USER_AGENT},
            timeout=_TIMEOUT_SECONDS,
            follow_redirects=True,
        ) as client:
            for site in websites:
                matches = await self._scrape_site(client, site, keywords)
                if matches:
                    items_extracted += len(matches)
                    saved_files.append(await self._save_matches(site, matches))

        return ScrapeResult(
            sites_visited=len(websites),
            items_extracted=items_extracted,
            saved_files=saved_files,
        )

    async def _scrape_site(
        self, client: httpx.AsyncClient, url: str, keywords: list[str]
    ) -> list[dict[str, str]]:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = [
            text for tag in soup.find_all(_TARGET_TAGS) if (text := tag.get_text(strip=True))
        ]

        if not keywords:
            return [{"url": url, "keyword": "", "text": paragraph} for paragraph in paragraphs]

        matches: list[dict[str, str]] = []
        for paragraph in paragraphs:
            for keyword in keywords:
                if keyword in paragraph:
                    matches.append({"url": url, "keyword": keyword, "text": paragraph})
                    break
        return matches

    async def _save_matches(self, url: str, matches: list[dict[str, str]]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        domain = urlparse(url).netloc.replace(".", "_") or "site"
        filename = f"{timestamp}_{domain}.jsonl"
        content = "\n".join(json.dumps(match, ensure_ascii=False) for match in matches)
        return await self._storage.save(filename, content)
