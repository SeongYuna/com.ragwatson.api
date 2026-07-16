from __future__ import annotations

from pydantic import BaseModel


class CrawlResponse(BaseModel):
    sites_visited: int
    pages_saved: int
    saved_files: list[str]
