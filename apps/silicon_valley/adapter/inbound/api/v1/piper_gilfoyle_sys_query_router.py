from fastapi import APIRouter, Depends, HTTPException

from silicon_valley.adapter.inbound.api.dependencies import get_piper_gilfoyle_sys_use_case
from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_sys_query_schema import PiperGilfoyleSysIntroduceResponse
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import PiperGilfoyleSysIntroduceQuery
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import PiperGilfoyleSysUseCase

piper_gilfoyle_sys_router = APIRouter(prefix="/silicon-valley/gilfoyle", tags=["/silicon-valley/gilfoyle"])


@piper_gilfoyle_sys_router.get("/myself", response_model=PiperGilfoyleSysIntroduceResponse)
async def introduce_myself(
    use_case: PiperGilfoyleSysUseCase = Depends(get_piper_gilfoyle_sys_use_case),
) -> PiperGilfoyleSysIntroduceResponse:
    try:
        result = await use_case.introduce_myself(
            PiperGilfoyleSysIntroduceQuery(id=2, name='Bertram Gilfoyle')
        )
        return PiperGilfoyleSysIntroduceResponse(id=result.id, name=result.name, message=result.message)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
