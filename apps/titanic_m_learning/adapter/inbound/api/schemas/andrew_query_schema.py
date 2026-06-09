"""Andrew READ — GET /titanic/andrew/table 전용 스키마."""

from pydantic import BaseModel, Field


class AndrewTableQuery(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=500)


class AndrewReadPassengerResponse(BaseModel):
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


class AndrewIntroduceSchema(BaseModel):
    id: int = Field(2, description="Andrew ID")
    name: str = Field('토마스 앤드류스 (Thomas Andrews)', description="Andrew name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": '토마스 앤드류스 (Thomas Andrews)',
            }
        }
    }


class AndrewIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
