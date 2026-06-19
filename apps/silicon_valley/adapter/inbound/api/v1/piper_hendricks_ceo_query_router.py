from fastapi import APIRouter, Depends, HTTPException

from silicon_valley.adapter.inbound.api.dependencies import get_piper_hendricks_ceo_use_case
from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_query_schema import PiperHendricksCeoIntroduceResponse
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import PiperHendricksCeoIntroduceQuery
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import PiperHendricksCeoUseCase

piper_hendricks_ceo_router = APIRouter(prefix="/silicon-valley/hendricks", tags=["/silicon-valley/hendricks"])


@piper_hendricks_ceo_router.get("/myself", response_model=PiperHendricksCeoIntroduceResponse)
async def introduce_myself(
    use_case: PiperHendricksCeoUseCase = Depends(get_piper_hendricks_ceo_use_case),
) -> PiperHendricksCeoIntroduceResponse:
    try:
        result = await use_case.introduce_myself(
            PiperHendricksCeoIntroduceQuery(id=1, name='Richard Hendricks')
        )
        return PiperHendricksCeoIntroduceResponse(id=result.id, name=result.name, message=result.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
