from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    id: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    nickname: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1)
    role: str = Field(default="user")
