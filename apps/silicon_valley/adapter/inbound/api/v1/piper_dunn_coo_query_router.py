from fastapi import APIRouter, Depends, HTTPException

from silicon_valley.adapter.inbound.api.dependencies import get_piper_dunn_coo_use_case
from silicon_valley.adapter.inbound.api.schemas.piper_dunn_coo_query_schema import PiperDunnCooIntroduceResponse
from silicon_valley.app.dtos.piper_dunn_coo_dto import PiperDunnCooIntroduceQuery
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import PiperDunnCooUseCase

piper_dunn_coo_router = APIRouter(prefix="/silicon-valley/dunn", tags=["/silicon-valley/dunn"])


@piper_dunn_coo_router.get("/myself", response_model=PiperDunnCooIntroduceResponse)
async def introduce_myself(
    use_case: PiperDunnCooUseCase = Depends(get_piper_dunn_coo_use_case),
) -> PiperDunnCooIntroduceResponse:
    try:
        result = await use_case.introduce_myself(
            PiperDunnCooIntroduceQuery(id=3, name='Donald Dunn')
        )
        return PiperDunnCooIntroduceResponse(id=result.id, name=result.name, message=result.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
