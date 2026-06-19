from pydantic import BaseModel, Field


class PiperDunnCooIntroduceSchema(BaseModel):
    id: int = Field(3, description="Dunn COO ID")
    name: str = Field('Donald Dunn', description="Dunn COO name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": 'Donald Dunn',
            }
        }
    }


class PiperDunnCooIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
