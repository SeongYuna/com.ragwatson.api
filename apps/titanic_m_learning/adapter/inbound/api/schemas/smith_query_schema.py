"""Smith READ — GET /titanic/smith/summary 전용 스키마."""

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
