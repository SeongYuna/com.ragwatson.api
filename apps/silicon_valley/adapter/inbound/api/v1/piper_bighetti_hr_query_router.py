from fastapi import APIRouter, Depends, HTTPException

from silicon_valley.adapter.inbound.api.dependencies import get_piper_bighetti_hr_use_case
from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_query_schema import PiperBighettiHrIntroduceResponse
from silicon_valley.app.dtos.piper_bighetti_hr_dto import PiperBighettiHrIntroduceQuery
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import PiperBighettiHrUseCase

piper_bighetti_hr_router = APIRouter(prefix="/silicon-valley/bighetti", tags=["/silicon-valley/bighetti"])


@piper_bighetti_hr_router.get("/myself", response_model=PiperBighettiHrIntroduceResponse)
async def introduce_myself(
    use_case: PiperBighettiHrUseCase = Depends(get_piper_bighetti_hr_use_case),
) -> PiperBighettiHrIntroduceResponse:
    try:
        result = await use_case.introduce_myself(
            PiperBighettiHrIntroduceQuery(id=5, name='Nelson Bighetti')
        )
        return PiperBighettiHrIntroduceResponse(id=result.id, name=result.name, message=result.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
