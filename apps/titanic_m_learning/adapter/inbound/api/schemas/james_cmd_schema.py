"""James WRITE — POST /titanic/james/upload 전용 스키마."""

from pydantic import BaseModel, Field


class JamesWritePassengerRequest(BaseModel):
    """CSV 1행. flat 12 fields, all str."""

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str = Field(alias="Sex")
    age: str = Field(alias="Age")
    sib_sp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(alias="Ticket")
    fare: str = Field(alias="Fare")
    cabin: str = Field(alias="Cabin")
    embarked: str = Field(alias="Embarked")

    model_config = {"populate_by_name": True}


class JamesWriteUploadResponse(BaseModel):
    """업로드 저장 결과."""

    count: int


class JamesIntroduceSchema(BaseModel):
    id: int = Field(4, description="James ID")
    name: str = Field('James', description="James name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": 'James',
            }
        }
    }


class JamesIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
