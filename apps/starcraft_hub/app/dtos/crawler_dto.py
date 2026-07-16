from __future__ import annotations

from pydantic import BaseModel


class CrawlResult(BaseModel):
    sites_visited: int
    pages_saved: int
    saved_files: list[str]
