"""Hartley READ — GET /titanic/hartley/sample 전용 스키마."""

from pydantic import BaseModel, Field


class HartleySampleQuery(BaseModel):
    count: int = Field(default=10, ge=1, le=100)


class HartleyReadPassengerResponse(BaseModel):
    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: int
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


class HartleyIntroduceSchema(BaseModel):
    id: int = Field(7, description="Hartley ID")
    name: str = Field('Wallace Hartley', description="Hartley name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 7,
                "name": 'Wallace Hartley',
            }
        }
    }


class HartleyIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
