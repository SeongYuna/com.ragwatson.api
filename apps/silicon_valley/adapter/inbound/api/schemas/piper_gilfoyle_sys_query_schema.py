from pydantic import BaseModel, Field


class PiperGilfoyleSysIntroduceSchema(BaseModel):
    id: int = Field(2, description="Gilfoyle Systems ID")
    name: str = Field('Bertram Gilfoyle', description="Gilfoyle Systems name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": 'Bertram Gilfoyle',
            }
        }
    }


class PiperGilfoyleSysIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
