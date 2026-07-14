from __future__ import annotations

from pydantic import BaseModel


class YoloInferenceCommand(BaseModel):
    image_bytes: bytes
    filename: str


class DetectedFace(BaseModel):
    label: str
    confidence: float


class YoloInferenceResult(BaseModel):
    filename: str
    faces: list[DetectedFace]
    message: str
