from pydantic import BaseModel


class SignupResponseData(BaseModel):
    id: str
    password: str
    nickname: str
    email: str
    role: str


class SignupResponse(BaseModel):
    ok: bool
    data: SignupResponseData
