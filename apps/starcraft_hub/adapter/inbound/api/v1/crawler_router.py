from __future__ import annotations

from fastapi import APIRouter, Depends

from starcraft_hub.adapter.inbound.api.schemas.crawler_schema import CrawlResponse
from starcraft_hub.app.ports.input.crawler_port import CrawlerPort
from starcraft_hub.dependencies.crawler_provider import get_crawler_use_case

router = APIRouter(prefix="/starcraft/crawler", tags=["starcraft"])


@router.post("/run", response_model=CrawlResponse)
async def run_crawler(
    use_case: CrawlerPort = Depends(get_crawler_use_case),
) -> CrawlResponse:
    result = await use_case.crawl()
    return CrawlResponse(
        sites_visited=result.sites_visited,
        pages_saved=result.pages_saved,
        saved_files=result.saved_files,
    )
