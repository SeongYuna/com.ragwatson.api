from __future__ import annotations

import json
import re

from core.lol.orchestrator_port import (
    OrchestratorMessage,
    OrchestratorPort,
    OrchestratorRequest,
)
from starcraft_hub.app.dtos.command_dto import ExecuteCommandCommand, ExecuteCommandResult
from starcraft_hub.app.ports.input.command_port import CommandPort
from starcraft_hub.app.ports.input.crawler_port import CrawlerPort
from starcraft_hub.app.ports.input.scrapper_port import ScrapperPort

_SYSTEM_PROMPT = """너는 사용자의 자연어 명령에서 웹 크롤링/스크래핑 작업을 추출하는 비서야.
아래 지정된 JSON 형식으로만 응답해. 다른 설명은 붙이지 마.

출력 JSON 스키마:
{"action": "crawl" | "scrape", "websites": ["https://..."], "keywords": ["단어1", "단어2"]}

[분류 기준]
- "크롤링", "크롤러", 여러 페이지·링크를 따라가는 요청: "crawl"
- "스크래핑", "스크랩", 특정 페이지에서 정보만 뽑는 요청: "scrape"
- 명령에 없는 키워드는 빈 배열로 둔다.

[예시]
명령: "https://example.com 크롤링해줘, 키워드는 스타크래프트"
답변: {"action": "crawl", "websites": ["https://example.com"], "keywords": ["스타크래프트"]}"""


class CommandInteractor(CommandPort):
    """자연어 명령을 LLM으로 해석해 이번에 파싱된 사이트/키워드만 즉시 크롤링/스크래핑한다.

    Redis에는 아무것도 기록하지 않는다(일회성 실행) — 매번 새로 파싱된 대상만 처리해
    등록된 사이트가 무한정 누적되는 것을 피한다.
    """

    def __init__(
        self,
        orchestrator: OrchestratorPort,
        crawler: CrawlerPort,
        scrapper: ScrapperPort,
    ) -> None:
        self._orchestrator = orchestrator
        self._crawler = crawler
        self._scrapper = scrapper

    async def execute(self, command: ExecuteCommandCommand) -> ExecuteCommandResult:
        parsed = await self._interpret(command.text)
        websites = self._as_str_list(parsed.get("websites"))
        keywords = self._as_str_list(parsed.get("keywords"))
        action = "scrape" if parsed.get("action") == "scrape" else "crawl"

        if action == "scrape":
            scrape_result = await self._scrapper.scrape(websites=websites, keywords=keywords)
            count = scrape_result.items_extracted
            saved_files = scrape_result.saved_files
        else:
            crawl_result = await self._crawler.crawl(websites=websites, keywords=keywords)
            count = crawl_result.pages_saved
            saved_files = crawl_result.saved_files

        return ExecuteCommandResult(
            action=action,
            websites=websites,
            keywords=keywords,
            count=count,
            saved_files=saved_files,
        )

    async def _interpret(self, text: str) -> dict[str, object]:
        request = OrchestratorRequest(
            messages=[
                OrchestratorMessage(role="system", content=_SYSTEM_PROMPT),
                OrchestratorMessage(role="user", content=text),
            ]
        )
        response = await self._orchestrator.chat(request)
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if not match:
            return {}
        try:
            parsed = json.loads(match.group())
        except json.JSONDecodeError:
            return {}
        return parsed if isinstance(parsed, dict) else {}

    @staticmethod
    def _as_str_list(value: object) -> list[str]:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, str)]
        return []
