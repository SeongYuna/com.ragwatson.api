from pydantic import BaseModel


class UserSchema(BaseModel):
    id: str
    password: str
    nickname: str
    email: str
    role: str


class UserLoginSchema(BaseModel):
    id: str
    password: str