"""Caledon READ — GET /titanic/cal/calculate 전용 스키마."""

from pydantic import BaseModel, Field


class CaledonReadStatsResponse(BaseModel):
    total: int
    survived: int
    deceased: int
    survival_rate: float


class CaledonIntroduceSchema(BaseModel):
    id: int = Field(11, description="Caledon ID")
    name: str = Field('Caledon Hockley', description="Caledon name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "name": 'Caledon Hockley',
            }
        }
    }


class CaledonIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
