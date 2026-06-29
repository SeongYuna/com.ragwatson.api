"""James WRITE — POST /titanic/james/upload 전용 스키마."""

from pydantic import BaseModel, Field


class JamesWritePassengerRequest(BaseModel):
    """CSV 1행. flat fields, all str. train(Survived O) · test(Survived X) 모두 허용."""

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(default="", alias="Survived")
    pclass: str = Field(default="", alias="Pclass")
    name: str = Field(default="", alias="Name")
    gender: str = Field(default="", alias="Sex")
    age: str = Field(default="", alias="Age")
    sib_sp: str = Field(default="0", alias="SibSp")
    parch: str = Field(default="0", alias="Parch")
    ticket: str = Field(default="", alias="Ticket")
    fare: str = Field(default="", alias="Fare")
    cabin: str = Field(default="", alias="Cabin")
    embarked: str = Field(default="", alias="Embarked")

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
