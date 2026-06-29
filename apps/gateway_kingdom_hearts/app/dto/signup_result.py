from dataclasses import dataclass


@dataclass(frozen=True)
class SignupResult:
    id: str
    password: str
    nickname: str
    email: str
    role: str
