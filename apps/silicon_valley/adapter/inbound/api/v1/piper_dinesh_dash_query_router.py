from fastapi import APIRouter, Depends, HTTPException

from silicon_valley.adapter.inbound.api.dependencies import get_piper_dinesh_dash_use_case
from silicon_valley.adapter.inbound.api.schemas.piper_dinesh_dash_query_schema import PiperDineshDashIntroduceResponse
from silicon_valley.app.dtos.piper_dinesh_dash_dto import PiperDineshDashIntroduceQuery
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import PiperDineshDashUseCase

piper_dinesh_dash_router = APIRouter(prefix="/silicon-valley/dinesh", tags=["/silicon-valley/dinesh"])


@piper_dinesh_dash_router.get("/myself", response_model=PiperDineshDashIntroduceResponse)
async def introduce_myself(
    use_case: PiperDineshDashUseCase = Depends(get_piper_dinesh_dash_use_case),
) -> PiperDineshDashIntroduceResponse:
    try:
        result = await use_case.introduce_myself(
            PiperDineshDashIntroduceQuery(id=4, name='Dinesh Chugtai')
        )
        return PiperDineshDashIntroduceResponse(id=result.id, name=result.name, message=result.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
