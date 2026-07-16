from __future__ import annotations

from pydantic import BaseModel


class ScrapeResponse(BaseModel):
    sites_visited: int
    items_extracted: int
    saved_files: list[str]
