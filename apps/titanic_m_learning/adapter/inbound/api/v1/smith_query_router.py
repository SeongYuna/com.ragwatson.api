from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_smith_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_query_mapper import stats_to_response
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicStatsResponse
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase

smith_query_router = APIRouter(prefix="/titanic/smith", tags=["/titanic/smith"])


@smith_query_router.get("/summary", response_model=TitanicStatsResponse)
async def get_passenger_summary(
    use_case: SmithUseCase = Depends(get_smith_use_case),
) -> TitanicStatsResponse:
    try:
        result = await use_case.get_summary()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return stats_to_response(result)
