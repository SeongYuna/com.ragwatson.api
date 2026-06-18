from dataclasses import dataclass


@dataclass(frozen=True)
class SmithStatsResult:
    total: int
    survived: int
    deceased: int
    survival_rate: float

@dataclass(frozen=True)
class SmithIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class SmithIntroduceResult:
    id: int
    name: str
    message: str


@dataclass(frozen=True)
class SmithChatMessageDto:
    role: str
    content: str


@dataclass(frozen=True)
class SmithChatQuery:
    messages: tuple[SmithChatMessageDto, ...]
    model: str | None


@dataclass(frozen=True)
class SmithChatResult:
    reply: str
