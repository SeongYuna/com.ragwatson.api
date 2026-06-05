from pydantic import BaseModel


class TitanicPassengerResponse(BaseModel):
    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: int  # 0=female, 1=male
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


class TitanicUploadResponse(BaseModel):
    count: int

class TitanicStatsResponse(BaseModel):
    total: int
    survived: int
    deceased: int
    survival_rate: float


class TitanicColumnResponse(BaseModel):
    name: str
    description: str
    role: str


class TitanicDatasetInfoResponse(BaseModel):
    columns: list[TitanicColumnResponse]