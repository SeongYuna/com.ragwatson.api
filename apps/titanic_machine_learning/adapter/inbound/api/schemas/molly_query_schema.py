"""Molly 스키마 — 자기소개 전용."""

from pydantic import BaseModel, Field


class MollyIntroduceSchema(BaseModel):
    id: int = Field(10, description="Molly ID")
    name: str = Field('Margaret Brown', description="Molly name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 10,
                "name": 'Margaret Brown',
            }
        }
    }


class MollyIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
