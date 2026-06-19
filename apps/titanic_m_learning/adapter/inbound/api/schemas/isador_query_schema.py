"""Isador 스키마 — 자기소개 전용."""

from pydantic import BaseModel, Field


class IsadorIntroduceSchema(BaseModel):
    id: int = Field(8, description="Isador ID")
    name: str = Field('Isidor Straus', description="Isador name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 8,
                "name": 'Isidor Straus',
            }
        }
    }


class IsadorIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
