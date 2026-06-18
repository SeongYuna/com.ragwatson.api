from fastapi import APIRouter, Depends, HTTPException, Query

from titanic_m_learning.adapter.inbound.api.dependencies import get_hartley_use_case
from titanic_m_learning.adapter.inbound.api.mappers.hartley_query_mapper import queries_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.hartley_query_schema import HartleyReadPassengerResponse
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.adapter.inbound.api.schemas.hartley_query_schema import HartleyIntroduceResponse
from titanic_m_learning.app.dtos.hartley_dto import HartleyIntroduceQuery

hartley_query_router = APIRouter(prefix="/titanic/hartley", tags=["/titanic/hartley"])


@hartley_query_router.get("/sample", response_model=list[HartleyReadPassengerResponse])
async def get_random_sample(
    count: int = Query(10, ge=1, le=100),
    use_case: HartleyUseCase = Depends(get_hartley_use_case),
) -> list[HartleyReadPassengerResponse]:
    try:
        queries = await use_case.sample(count=count)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return queries_to_responses(queries)

@hartley_query_router.get("/myself", response_model=HartleyIntroduceResponse)
async def introduce_myself(
    use_case: HartleyUseCase = Depends(get_hartley_use_case),
) -> HartleyIntroduceResponse:
    result = await use_case.introduce_myself(HartleyIntroduceQuery(id=7, name='Wallace Hartley'))
    return HartleyIntroduceResponse(id=result.id, name=result.name, message=result.message)

