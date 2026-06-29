"""Smith READ/CHAT — /titanic/smith/* 전용 스키마."""

from typing import Literal

from pydantic import BaseModel, Field


class SmithReadStatsResponse(BaseModel):
    total: int
    survived: int
    deceased: int
    survival_rate: float


class SmithIntroduceSchema(BaseModel):
    id: int = Field(5, description="Smith ID")
    name: str = Field('에드워드 스미스 (Edward Smith)', description="Smith name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": '에드워드 스미스 (Edward Smith)',
            }
        }
    }


class SmithIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str


class SmithChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, description="채팅 메시지 본문")


class SmithChatRequest(BaseModel):
    """사용자가 POST로 채팅창에 입력한 자연어 대화 내역."""

    messages: list[SmithChatMessage] = Field(..., min_length=1)
    model: str | None = Field(None, description="Gemini 모델 ID (미지정 시 서버 기본값)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [
                    {"role": "user", "content": "1등석 승객 생존률이 어땠나요?"},
                ],
                "model": "gemini-2.5-flash",
            }
        }
    }


class SmithChatResponse(BaseModel):
    reply: str
