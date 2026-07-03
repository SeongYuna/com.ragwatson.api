from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from lenna_vision.adapter.inbound.api.dependencies import get_lenna_vision_use_case
from lenna_vision.adapter.inbound.api.schemas.lenna_vision_query_schema import (
    LennaImageUploadResponse,
    LennaVisionIntroduceResponse,
)
from lenna_vision.app.ports.input.lenna_vision_use_case import LennaVisionUseCase
from lenna_vision.app.dtos.lenna_vision_dto import LennaImageUploadCommand, LennaVisionIntroduceQuery

_ALLOWED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")

lenna_vision_query_router = APIRouter(prefix="/lenna_vision", tags=["/lenna_vision"])


@lenna_vision_query_router.get("/myself", response_model=LennaVisionIntroduceResponse)
async def introduce_myself(
    use_case: LennaVisionUseCase = Depends(get_lenna_vision_use_case),
) -> LennaVisionIntroduceResponse:
    result = await use_case.introduce_myself(LennaVisionIntroduceQuery(id=1, name='LennaVision'))
    return LennaVisionIntroduceResponse(id=result.id, name=result.name, message=result.message)


@lenna_vision_query_router.post("/upload", response_model=LennaImageUploadResponse)
async def upload_image(
    file: UploadFile = File(...),
    use_case: LennaVisionUseCase = Depends(get_lenna_vision_use_case),
) -> LennaImageUploadResponse:
    if not file.filename or not file.filename.lower().endswith(_ALLOWED_EXTENSIONS):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드할 수 있습니다.")

    content = await file.read()
    try:
        result = await use_case.upload_image(
            LennaImageUploadCommand(filename=file.filename, content=content)
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return LennaImageUploadResponse(filename=result.filename, size=result.size, url=result.path)
