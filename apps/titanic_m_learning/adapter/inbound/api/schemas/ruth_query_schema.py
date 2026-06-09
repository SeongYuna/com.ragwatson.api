"""Ruth READ — GET /titanic/ruth/first-class 전용 스키마."""

from pydantic import BaseModel, Field


class RuthReadPassengerResponse(BaseModel):
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
