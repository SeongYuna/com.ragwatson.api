from __future__ import annotations

from pydantic import BaseModel


class YoloTrainCommand(BaseModel):
    epochs: int = 50
    batch: int = 16
    imgsz: int = 640
    device: int | str = 0  # 0 = GPU, "cpu" = CPU


class YoloTrainResult(BaseModel):
    success: bool
    best_model_path: str
    epochs_completed: int
    message: str
