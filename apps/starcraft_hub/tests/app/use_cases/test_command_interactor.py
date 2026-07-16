from unittest.mock import AsyncMock, MagicMock

import pytest

from core.lol.orchestrator_port import OrchestratorResponse
from starcraft_hub.app.dtos.command_dto import ExecuteCommandCommand
from starcraft_hub.app.dtos.crawler_dto import CrawlResult
from starcraft_hub.app.dtos.scrapper_dto import ScrapeResult
from starcraft_hub.app.use_cases.command_interactor import CommandInteractor


def _llm_response(content: str) -> OrchestratorResponse:
    return OrchestratorResponse(content=content, model="exaone3.5:2.4b")


@pytest.fixture
def mock_orchestrator():
    orchestrator = MagicMock()
    orchestrator.chat = AsyncMock()
    return orchestrator


@pytest.fixture
def mock_crawler():
    crawler = MagicMock()
    crawler.crawl = AsyncMock(
        return_value=CrawlResult(sites_visited=1, pages_saved=2, saved_files=["a.jsonl"])
    )
    return crawler


@pytest.fixture
def mock_scrapper():
    scrapper = MagicMock()
    scrapper.scrape = AsyncMock(
        return_value=ScrapeResult(sites_visited=1, items_extracted=3, saved_files=["b.jsonl"])
    )
    return scrapper


@pytest.fixture
def interactor(mock_orchestrator, mock_crawler, mock_scrapper):
    return CommandInteractor(
        orchestrator=mock_orchestrator, crawler=mock_crawler, scrapper=mock_scrapper
    )


class TestExecute:
    async def test_crawl_action_delegates_to_crawler_with_parsed_args(
        self, interactor, mock_orchestrator, mock_crawler, mock_scrapper
    ):
        mock_orchestrator.chat.return_value = _llm_response(
            '{"action": "crawl", "websites": ["https://example.com"], "keywords": ["스타크래프트"]}'
        )

        result = await interactor.execute(ExecuteCommandCommand(text="크롤링해줘"))

        mock_crawler.crawl.assert_awaited_once_with(
            websites=["https://example.com"], keywords=["스타크래프트"]
        )
        mock_scrapper.scrape.assert_not_awaited()
        assert result.action == "crawl"
        assert result.count == 2
        assert result.saved_files == ["a.jsonl"]

    async def test_scrape_action_delegates_to_scrapper_with_parsed_args(
        self, interactor, mock_orchestrator, mock_crawler, mock_scrapper
    ):
        mock_orchestrator.chat.return_value = _llm_response(
            '{"action": "scrape", "websites": ["https://example.com"], "keywords": []}'
        )

        result = await interactor.execute(ExecuteCommandCommand(text="스크래핑해줘"))

        mock_scrapper.scrape.assert_awaited_once_with(
            websites=["https://example.com"], keywords=[]
        )
        mock_crawler.crawl.assert_not_awaited()
        assert result.action == "scrape"
        assert result.count == 3
        assert result.saved_files == ["b.jsonl"]

    async def test_defaults_to_crawl_when_action_missing(
        self, interactor, mock_orchestrator, mock_crawler
    ):
        mock_orchestrator.chat.return_value = _llm_response(
            '{"websites": ["https://example.com"]}'
        )

        result = await interactor.execute(ExecuteCommandCommand(text="애매한 명령"))

        assert result.action == "crawl"
        mock_crawler.crawl.assert_awaited_once_with(
            websites=["https://example.com"], keywords=[]
        )

    async def test_empty_result_when_llm_response_has_no_json(
        self, interactor, mock_orchestrator, mock_crawler
    ):
        mock_orchestrator.chat.return_value = _llm_response("죄송하지만 이해하지 못했어요.")

        result = await interactor.execute(ExecuteCommandCommand(text="???"))

        assert result.websites == []
        assert result.keywords == []
        mock_crawler.crawl.assert_awaited_once_with(websites=[], keywords=[])

    async def test_ignores_non_string_items_in_parsed_lists(
        self, interactor, mock_orchestrator, mock_crawler
    ):
        mock_orchestrator.chat.return_value = _llm_response(
            '{"action": "crawl", "websites": ["https://example.com", 1], "keywords": [true]}'
        )

        result = await interactor.execute(ExecuteCommandCommand(text="크롤링해줘"))

        assert result.websites == ["https://example.com"]
        assert result.keywords == []
