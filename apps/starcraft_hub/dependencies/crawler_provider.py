from __future__ import annotations

from pathlib import Path

from starcraft_hub.adapter.outbound.filesystem.local_file_storage_repo import (
    LocalFileStorageRepo,
)
from starcraft_hub.adapter.outbound.redis.web_source_redis_repo import WebSourceRedisRepo
from starcraft_hub.app.ports.input.crawler_port import CrawlerPort
from starcraft_hub.app.use_cases.crawler_interactor import CrawlerInteractor
from starcraft_hub.dependencies.redis_client import get_redis_client

_CRAWLED_DIR = Path(__file__).resolve().parents[3] / "resources" / "crawled"


def get_crawler_use_case() -> CrawlerPort:
    return CrawlerInteractor(
        web_source=WebSourceRedisRepo(redis_client=get_redis_client(), namespace="crawler"),
        storage=LocalFileStorageRepo(base_dir=_CRAWLED_DIR),
    )
