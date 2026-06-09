from dataclasses import dataclass


@dataclass(frozen=True)
class RoseColumnInfo:
    name: str
    description: str
    role: str


@dataclass(frozen=True)
class RoseDatasetInfoResult:
    columns: tuple[RoseColumnInfo, ...]

@dataclass(frozen=True)
class RoseIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RoseIntroduceResult:
    id: int
    name: str
    message: str
