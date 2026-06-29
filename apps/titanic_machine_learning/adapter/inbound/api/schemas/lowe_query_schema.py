"""Lowe READ — 구명보트·구조 관련 조회 전용 스키마."""

from pydantic import BaseModel, Field


class LoweReadLifeboatQuery(BaseModel):
    """GET /titanic/lowe/lifeboats 쿼리 파라미터."""

    lifeboat: str | None = Field(default=None, min_length=1)


class LoweReadLifeboatPassengerResponse(BaseModel):
    """구명보트 탑승 승객 1행."""

    passenger_id: str
    name: str
    lifeboat: str
    survived: str
    gender: int
    pclass: str


class LoweIntroduceSchema(BaseModel):
    id: int = Field(9, description="Lowe ID")
    name: str = Field('Harold Lowe', description="Lowe name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 9,
                "name": 'Harold Lowe',
            }
        }
    }


class LoweIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
