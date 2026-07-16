from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from starcraft_hub.app.use_cases.scrapper_interactor import ScrapperInteractor

_SITE_HTML = """
<html><body>
<p>스타크래프트 프로게이머 소식</p>
<p>아무 관련 없는 문단</p>
<li>스타크래프트 리그 일정</li>
</body></html>
"""


class _FakeResponse:
    def __init__(self, text: str, status_error: bool = False) -> None:
        self.text = text
        self._status_error = status_error

    def raise_for_status(self) -> None:
        if self._status_error:
            raise httpx.HTTPStatusError("error", request=MagicMock(), response=MagicMock())


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
    return ScrapperInteractor(web_source=mock_web_source, storage=mock_storage)


class TestScrape:
    async def test_extracts_keyword_matched_paragraphs(
        self, interactor, mock_storage, monkeypatch
    ):
        async def fake_get(self, url, *args, **kwargs):
            return _FakeResponse(_SITE_HTML)

        monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

        result = await interactor.scrape()

        assert result.sites_visited == 1
        assert result.items_extracted == 2
        mock_storage.save.assert_awaited_once()
        filename, content = mock_storage.save.call_args.args
        assert filename.endswith(".jsonl")
        assert len([line for line in content.strip().split("\n") if line]) == 2

    async def test_uses_explicit_websites_and_keywords_when_provided(
        self, interactor, mock_web_source, monkeypatch
    ):
        async def fake_get(self, url, *args, **kwargs):
            return _FakeResponse(_SITE_HTML)

        monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

        await interactor.scrape(websites=["https://example.com/"], keywords=["스타크래프트"])

        mock_web_source.get_websites.assert_not_awaited()
        mock_web_source.get_keywords.assert_not_awaited()

    async def test_no_matches_when_keyword_absent(self, interactor, mock_storage, monkeypatch):
        async def fake_get(self, url, *args, **kwargs):
            return _FakeResponse("<html><body><p>관련 없음</p></body></html>")

        monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

        result = await interactor.scrape()

        assert result.items_extracted == 0
        mock_storage.save.assert_not_awaited()

    async def test_skips_site_on_http_error(self, interactor, mock_storage, monkeypatch):
        async def fake_get(self, url, *args, **kwargs):
            return _FakeResponse("", status_error=True)

        monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)

        result = await interactor.scrape()

        assert result.sites_visited == 1
        assert result.items_extracted == 0
        mock_storage.save.assert_not_awaited()
