from dataclasses import dataclass


@dataclass(frozen=True)
class PiperHendricksCeoIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperHendricksCeoIntroduceResult:
    id: int
    name: str
    message: str
