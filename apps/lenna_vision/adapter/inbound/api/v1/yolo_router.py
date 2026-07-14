from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from lenna_vision.app.dtos.yolo_inference_dto import YoloInferenceCommand, YoloInferenceResult
from lenna_vision.app.ports.input.yolo_inference_use_case import YoloInferenceUseCase
from lenna_vision.dependencies.yolo_inference_provider import get_yolo_inference_use_case

yolo_router = APIRouter(prefix="/lenna_vision/yolo", tags=["yolo"])


@yolo_router.post("/predict", response_model=YoloInferenceResult)
async def predict(
    file: UploadFile = File(...),
    use_case: YoloInferenceUseCase = Depends(get_yolo_inference_use_case),
) -> YoloInferenceResult:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    image_bytes = await file.read()
    command = YoloInferenceCommand(
        image_bytes=image_bytes,
        filename=file.filename or "unknown",
    )
    return use_case.predict(command)
