from __future__ import annotations

from fastapi import APIRouter, Depends

from starcraft_hub.adapter.inbound.api.schemas.scrapper_schema import ScrapeResponse
from starcraft_hub.app.ports.input.scrapper_port import ScrapperPort
from starcraft_hub.dependencies.scrapper_provider import get_scrapper_use_case

router = APIRouter(prefix="/starcraft/scrapper", tags=["starcraft"])


@router.post("/run", response_model=ScrapeResponse)
async def run_scrapper(
    use_case: ScrapperPort = Depends(get_scrapper_use_case),
) -> ScrapeResponse:
    result = await use_case.scrape()
    return ScrapeResponse(
        sites_visited=result.sites_visited,
        items_extracted=result.items_extracted,
        saved_files=result.saved_files,
    )
