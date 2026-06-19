from pydantic import BaseModel, Field


class PiperHendricksCeoIntroduceSchema(BaseModel):
    id: int = Field(1, description="Hendricks CEO ID")
    name: str = Field('Richard Hendricks', description="Hendricks CEO name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": 'Richard Hendricks',
            }
        }
    }


class PiperHendricksCeoIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
