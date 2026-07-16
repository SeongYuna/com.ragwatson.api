from __future__ import annotations

import json
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from starcraft_hub.app.dtos.crawler_dto import CrawlResult
from starcraft_hub.app.ports.input.crawler_port import CrawlerPort
from starcraft_hub.app.ports.output.result_storage_port import ResultStoragePort
from starcraft_hub.app.ports.output.web_source_port import WebSourcePort

_MAX_PAGES_PER_SITE = 10
_TIMEOUT_SECONDS = 10.0
_USER_AGENT = "StarcraftHubCrawler/1.0"


class CrawlerInteractor(CrawlerPort):
    """Redis에 등록된 웹사이트를 시드로 같은 도메인 링크를 순회해 페이지를 수집한다.

    사이트당 방문 페이지를 _MAX_PAGES_PER_SITE로 제한해 무한 크롤링을 막는다.
    사이트별로 방문한 페이지를 한 줄씩 담은 .jsonl 파일 하나로 저장한다.
    """

    def __init__(self, web_source: WebSourcePort, storage: ResultStoragePort) -> None:
        self._web_source = web_source
        self._storage = storage

    async def crawl(
        self,
        websites: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> CrawlResult:
        if websites is None:
            websites = await self._web_source.get_websites()
        if keywords is None:
            keywords = await self._web_source.get_keywords()

        saved_files: list[str] = []
        pages_saved = 0
        async with httpx.AsyncClient(
            headers={"User-Agent": _USER_AGENT},
            timeout=_TIMEOUT_SECONDS,
            follow_redirects=True,
        ) as client:
            for site in websites:
                pages = await self._crawl_site(client, site, keywords)
                if pages:
                    pages_saved += len(pages)
                    saved_files.append(await self._save_site(site, pages))

        return CrawlResult(
            sites_visited=len(websites),
            pages_saved=pages_saved,
            saved_files=saved_files,
        )

    async def _crawl_site(
        self, client: httpx.AsyncClient, seed_url: str, keywords: list[str]
    ) -> list[dict[str, str]]:
        domain = urlparse(seed_url).netloc
        visited: set[str] = set()
        queue: list[str] = [seed_url]
        pages: list[dict[str, str]] = []

        while queue and len(visited) < _MAX_PAGES_PER_SITE:
            url = queue.pop(0)
            if url in visited:
                continue
            visited.add(url)

            html = await self._fetch(client, url)
            if html is None:
                continue

            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text(separator="\n", strip=True)

            if keywords and not any(keyword in text for keyword in keywords):
                continue

            pages.append({"url": url, "text": text})

            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link["href"])
                if urlparse(next_url).netloc == domain and next_url not in visited:
                    queue.append(next_url)

        return pages

    @staticmethod
    async def _fetch(client: httpx.AsyncClient, url: str) -> str | None:
        try:
            response = await client.get(url)
            response.raise_for_status()
        except httpx.HTTPError:
            return None
        return response.text

    async def _save_site(self, seed_url: str, pages: list[dict[str, str]]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        domain = urlparse(seed_url).netloc.replace(".", "_") or "site"
        filename = f"{timestamp}_{domain}.jsonl"
        content = "\n".join(json.dumps(page, ensure_ascii=False) for page in pages)
        return await self._storage.save(filename, content)
