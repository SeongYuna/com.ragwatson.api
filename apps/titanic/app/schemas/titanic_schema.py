from typing import Literal

from pydantic import BaseModel, Field


class TitanicPassengerSchema(BaseModel):
    """CSV 한 행 API 응답용."""

    PassengerId: int | None = None
    Survived: int | None = None
    Pclass: int | None = None
    Name: str | None = None
    Sex: str | None = None
    Age: float | None = None
    SibSp: int | None = None
    Parch: int | None = None
    Ticket: str | None = None
    Fare: float | None = None
    Cabin: str | None = None
    Embarked: str | None = None


class TitanicCountSchema(BaseModel):
    count: int


class TitanicTreeStatusSchema(BaseModel):
    tree: bool


class TitanicModelSchema(BaseModel):
    model: str | None


class TitanicTrainResultSchema(BaseModel):
    trained: bool = True
    model_path: str


class TitanicColumnDocSchema(BaseModel):
    name: str
    description: str
    role: Literal["target", "feature", "meta"]


class TitanicDatasetInfoSchema(BaseModel):
    voyage: str = Field(
        default="1912-04-10 Southampton 출발 → 1912-04-15 침몰",
    )
    problem_type: str = Field(
        default="이진 분류 (6개 독립변수 → Survived 예측)",
    )
    target: str = "Survived"
    features: list[str] = Field(
        default_factory=lambda: ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"],
    )
    columns: list[TitanicColumnDocSchema] = Field(default_factory=list)
