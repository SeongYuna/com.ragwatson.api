"""Isador READ — GET /titanic/isador/families 전용 스키마."""

from pydantic import BaseModel, Field


class IsadorReadPassengerResponse(BaseModel):
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
