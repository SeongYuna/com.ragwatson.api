from dataclasses import dataclass


@dataclass(frozen=True)
class PiperGilfoyleSysIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class PiperGilfoyleSysIntroduceResult:
    id: int
    name: str
    message: str
