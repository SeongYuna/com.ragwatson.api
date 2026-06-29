"""Ruth 스키마 — 자기소개 전용."""

from pydantic import BaseModel, Field


class RuthIntroduceSchema(BaseModel):
    id: int = Field(6, description="Ruth ID")
    name: str = Field('Ruth', description="Ruth name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": 'Ruth',
            }
        }
    }


class RuthIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
