"""Molly READ — 주목 승객·생존자 프로필 조회 전용 스키마."""

from pydantic import BaseModel, Field


class MollyReadNotableSurvivorResponse(BaseModel):
    """주목 승객 1행 (Molly Brown 등 생존·연대 관련)."""

    passenger_id: str
    name: str
    pclass: str
    survived: str
    gender: int
    assistance_note: str


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
