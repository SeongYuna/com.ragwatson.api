from __future__ import annotations

from pathlib import Path

from starcraft_hub.app.ports.output.result_storage_port import ResultStoragePort


class LocalFileStorageRepo(ResultStoragePort):
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._base_dir.mkdir(parents=True, exist_ok=True)

    async def save(self, filename: str, content: str) -> str:
        path = self._base_dir / filename
        path.write_text(content, encoding="utf-8")
        return str(path)
