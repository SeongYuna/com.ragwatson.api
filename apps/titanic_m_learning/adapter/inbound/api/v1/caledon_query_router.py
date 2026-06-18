from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_caledon_use_case
from titanic_m_learning.adapter.inbound.api.mappers.cal_query_mapper import stats_to_response
from titanic_m_learning.adapter.inbound.api.schemas.cal_query_schema import CaledonReadStatsResponse
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.adapter.inbound.api.schemas.cal_query_schema import CaledonIntroduceResponse
from titanic_m_learning.app.dtos.caledon_dto import CaledonIntroduceQuery

cal_query_router = APIRouter(prefix="/titanic/cal", tags=["/titanic/cal"])


@cal_query_router.get("/calculate", response_model=CaledonReadStatsResponse)
async def calculate_survival_stats(
    use_case: CaledonUseCase = Depends(get_caledon_use_case),
) -> CaledonReadStatsResponse:
    try:
        result = await use_case.calculate_stats()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return stats_to_response(result)

@cal_query_router.get("/myself", response_model=CaledonIntroduceResponse)
async def introduce_myself(
    use_case: CaledonUseCase = Depends(get_caledon_use_case),
) -> CaledonIntroduceResponse:
    result = await use_case.introduce_myself(CaledonIntroduceQuery(id=11, name='Caledon Hockley'))
    return CaledonIntroduceResponse(id=result.id, name=result.name, message=result.message)

