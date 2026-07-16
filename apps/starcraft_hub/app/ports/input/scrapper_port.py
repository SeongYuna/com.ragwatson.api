from __future__ import annotations

from abc import ABC, abstractmethod

from starcraft_hub.app.dtos.scrapper_dto import ScrapeResult


class ScrapperPort(ABC):
    @abstractmethod
    async def scrape(
        self,
        websites: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> ScrapeResult:
        """websites/keywords를 생략하면 Redis에 등록된 전체 목록을 대상으로 실행한다.

        지정하면 그 값만 일회성으로 처리하고 Redis는 건드리지 않는다.
        """
        ...
