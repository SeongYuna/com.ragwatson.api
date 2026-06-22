"""Walter READ — GET /titanic/walter/table 전용 스키마."""

from pydantic import BaseModel, Field


class WalterReadPassengerResponse(BaseModel):
    """목록 조회 1행. gender: 0=female, 1=male."""

    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


class WalterIntroduceSchema(BaseModel):
    id: int = Field(1, description="Walter ID")
    name: str = Field('Walter', description="Walter name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": 'Walter',
            }
        }
    }


class WalterIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
