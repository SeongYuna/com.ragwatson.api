from fastapi import APIRouter, Depends, HTTPException, Query

from titanic_m_learning.adapter.inbound.api.dependencies import get_lowe_use_case
from titanic_m_learning.adapter.inbound.api.mappers.lowe_query_mapper import result_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.lowe_query_schema import LoweReadLifeboatPassengerResponse
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.adapter.inbound.api.schemas.lowe_query_schema import LoweIntroduceResponse
from titanic_m_learning.app.dtos.lowe_dto import LoweIntroduceQuery

lowe_query_router = APIRouter(prefix="/titanic/lowe", tags=["/titanic/lowe"])


@lowe_query_router.get("/lifeboats", response_model=list[LoweReadLifeboatPassengerResponse])
async def get_lifeboat_passengers(
    lifeboat: str | None = Query(default=None, min_length=1),
    use_case: LoweUseCase = Depends(get_lowe_use_case),
) -> list[LoweReadLifeboatPassengerResponse]:
    try:
        result = await use_case.find_lifeboats(lifeboat=lifeboat)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return result_to_responses(result)

@lowe_query_router.get("/myself", response_model=LoweIntroduceResponse)
async def introduce_myself(
    use_case: LoweUseCase = Depends(get_lowe_use_case),
) -> LoweIntroduceResponse:
    result = await use_case.introduce_myself(LoweIntroduceQuery(id=9, name='Harold Lowe'))
    return LoweIntroduceResponse(id=result.id, name=result.name, message=result.message)

