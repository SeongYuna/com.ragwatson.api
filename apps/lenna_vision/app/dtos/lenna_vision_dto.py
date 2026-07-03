from dataclasses import dataclass


@dataclass(frozen=True)
class LennaVisionIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class LennaVisionIntroduceResult:
    id: int
    name: str
    message: str


@dataclass(frozen=True)
class LennaImageUploadCommand:
    filename: str
    content: bytes


@dataclass(frozen=True)
class LennaImageUploadResult:
    filename: str
    size: int
    path: str
