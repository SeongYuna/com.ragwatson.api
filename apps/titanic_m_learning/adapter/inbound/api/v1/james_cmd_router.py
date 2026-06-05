import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from titanic_m_learning.adapter.inbound.api.dependencies import get_james_cmd_use_case
from titanic_m_learning.adapter.inbound.api.mappers.james_cmd_mapper import upload_result_to_response
from titanic_m_learning.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRequest
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicUploadResponse
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase

james_cmd_router = APIRouter(prefix="/titanic/james", tags=["/titanic/james"])


@james_cmd_router.post("/upload", response_model=TitanicUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesCmdUseCase = Depends(get_james_cmd_use_case),
) -> TitanicUploadResponse:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    raw = await file.read()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp949", errors="replace")

    reader = csv.DictReader(io.StringIO(text))
    requests: list[TitanicPassengerRequest] = []

    for line_num, row in enumerate(reader, start=2):
        try:
            requests.append(TitanicPassengerRequest.model_validate(row))
        except Exception as exc:
            raise HTTPException(
                status_code=422, detail=f"{line_num}행 파싱 오류: {exc}"
            ) from exc

    try:
        result = await use_case.execute(requests)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc

    return upload_result_to_response(result)
