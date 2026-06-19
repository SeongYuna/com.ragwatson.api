from pydantic import BaseModel, Field


class PiperBighettiHrIntroduceSchema(BaseModel):
    id: int = Field(5, description="Bighetti HR ID")
    name: str = Field('Nelson Bighetti', description="Bighetti HR name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": 'Nelson Bighetti',
            }
        }
    }


class PiperBighettiHrIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
