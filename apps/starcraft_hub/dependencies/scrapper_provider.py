from __future__ import annotations

from pathlib import Path

from starcraft_hub.adapter.outbound.filesystem.local_file_storage_repo import (
    LocalFileStorageRepo,
)
from starcraft_hub.adapter.outbound.redis.web_source_redis_repo import WebSourceRedisRepo
from starcraft_hub.app.ports.input.scrapper_port import ScrapperPort
from starcraft_hub.app.use_cases.scrapper_interactor import ScrapperInteractor
from starcraft_hub.dependencies.redis_client import get_redis_client

_SCRAPED_DIR = Path(__file__).resolve().parents[3] / "resources" / "scraped"


def get_scrapper_use_case() -> ScrapperPort:
    return ScrapperInteractor(
        web_source=WebSourceRedisRepo(redis_client=get_redis_client(), namespace="scrapper"),
        storage=LocalFileStorageRepo(base_dir=_SCRAPED_DIR),
    )
