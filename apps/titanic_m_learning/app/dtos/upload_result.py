from dataclasses import dataclass


@dataclass(frozen=True)
class UploadResult:
    count: int
