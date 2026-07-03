"""LennaVision 스키마 — 자기소개 · 이미지 업로드."""

from pydantic import BaseModel, Field


class LennaVisionIntroduceSchema(BaseModel):
    id: int = Field(1, description="LennaVision ID")
    name: str = Field('LennaVision', description="LennaVision name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": 'LennaVision',
            }
        }
    }


class LennaVisionIntroduceResponse(BaseModel):
    id: int
    name: str
    message: str


class LennaImageUploadResponse(BaseModel):
    filename: str
    size: int
    url: str
