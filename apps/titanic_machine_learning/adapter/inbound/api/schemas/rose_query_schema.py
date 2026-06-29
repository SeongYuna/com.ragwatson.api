"""Rose READ — GET /titanic/rose/info 전용 스키마."""

from pydantic import BaseModel, Field


class RoseReadColumnResponse(BaseModel):
    name: str
    description: str
    role: str


class RoseReadDatasetInfoResponse(BaseModel):
    columns: list[RoseReadColumnResponse]


class RoseIntroduceSchema(BaseModel):
    id: int = Field(12, description="Rose ID")
    name: str = Field('Rose DeWitt Bukater', description="Rose name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 12,
                "name": 'Rose DeWitt Bukater',
            }
        }
    }


class RoseIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
