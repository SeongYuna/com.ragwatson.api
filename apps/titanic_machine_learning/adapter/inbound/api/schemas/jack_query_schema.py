"""Jack READ — GET /titanic/jack/passenger/{passenger_id} 전용 스키마."""

from pydantic import BaseModel, Field


class JackPassengerPath(BaseModel):
    passenger_id: str = Field(min_length=1)


class JackReadPassengerResponse(BaseModel):
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


class JackIntroduceSchema(BaseModel):
    id: int = Field(3, description="Jack ID")
    name: str = Field('Jack Dawson', description="Jack name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": 'Jack Dawson',
            }
        }
    }


class JackIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
