from dataclasses import dataclass


@dataclass(frozen=True)
class ColumnInfo:
    name: str
    description: str
    role: str


@dataclass(frozen=True)
class DatasetInfoResult:
    columns: tuple[ColumnInfo, ...]
