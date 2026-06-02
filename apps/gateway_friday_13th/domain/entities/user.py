from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    password: str
    nickname: str
    email: str
    role: str

    @classmethod
    def create(
        cls,
        *,
        id: str,
        password: str,
        nickname: str,
        email: str,
        role: str = "user",
    ) -> "User":
        return cls(
            id=id,
            password=password,
            nickname=nickname,
            email=email,
            role=role,
        )
