from pydantic import BaseModel, Field


class PiperDineshDashIntroduceSchema(BaseModel):
    id: int = Field(4, description="Dinesh Dash ID")
    name: str = Field('Dinesh Chugtai', description="Dinesh Dash name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": 'Dinesh Chugtai',
            }
        }
    }


class PiperDineshDashIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str
