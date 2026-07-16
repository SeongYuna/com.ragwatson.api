from unittest.mock import AsyncMock, MagicMock

import pytest

from starcraft_hub.app.use_cases.crawler_interactor import CrawlerInteractor

_SEED_HTML = """
<html><body>
<p>스타크래프트 프로게이머 소식</p>
<a href="/page2">다음</a>
<a href="https://other.com/x">외부</a>
</body></html>
"""

_PAGE2_HTML = """
<html><body>
<p>스타크래프트 리그 결과</p>
</body></html>
"""

_NO_MATCH_HTML = "<html><body><p>아무 관련 없는 내용</p></body></html>"

_PAGES = {
    "https://example.com/": _SEED_HTML,
    "https://example.com/page2": _PAGE2_HTML,
}


async def _fake_fetch(client, url):
    return _PAGES.get(url)


@pytest.fixture
def mock_web_source():
    web_source = MagicMock()
    web_source.get_websites = AsyncMock(return_value=["https://example.com/"])
    web_source.get_keywords = AsyncMock(return_value=["스타크래프트"])
    return web_source


@pytest.fixture
def mock_storage():
    storage = MagicMock()
    storage.save = AsyncMock(return_value="saved/path.jsonl")
    return storage


@pytest.fixture
def interactor(mock_web_source, mock_storage):
    return CrawlerInteractor(web_source=mock_web_source, storage=mock_storage)


class TestCrawl:
    async def test_follows_same_domain_links_and_saves_jsonl(
        self, interactor, mock_storage, monkeypatch
    ):
        monkeypatch.setattr(CrawlerInteractor, "_fetch", staticmethod(_fake_fetch))

        result = await interactor.crawl()

        assert result.sites_visited == 1
        assert result.pages_saved == 2
        mock_storage.save.assert_awaited_once()
        filename, content = mock_storage.save.call_args.args
        assert filename.endswith(".jsonl")
        assert len(content.strip().split("\n")) == 2

    async def test_uses_explicit_websites_and_keywords_when_provided(
        self, interactor, mock_web_source, monkeypatch
    ):
        monkeypatch.setattr(CrawlerInteractor, "_fetch", staticmethod(_fake_fetch))

        await interactor.crawl(websites=["https://example.com/"], keywords=["스타크래프트"])

        mock_web_source.get_websites.assert_not_awaited()
        mock_web_source.get_keywords.assert_not_awaited()

    async def test_skips_pages_without_matching_keyword(
        self, interactor, mock_storage, monkeypatch
    ):
        async def fetch_no_match(client, url):
            return _NO_MATCH_HTML if url == "https://example.com/" else None

        monkeypatch.setattr(CrawlerInteractor, "_fetch", staticmethod(fetch_no_match))

        result = await interactor.crawl()

        assert result.pages_saved == 0
        mock_storage.save.assert_not_awaited()

    async def test_saves_all_pages_when_no_keywords(
        self, interactor, mock_web_source, mock_storage, monkeypatch
    ):
        mock_web_source.get_keywords = AsyncMock(return_value=[])
        monkeypatch.setattr(CrawlerInteractor, "_fetch", staticmethod(_fake_fetch))

        result = await interactor.crawl()

        assert result.pages_saved == 2
