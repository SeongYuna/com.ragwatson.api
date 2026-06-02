import logging

from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_caledon_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_mapper import stats_to_response
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicStatsResponse
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase

log = logging.getLogger("titanic.read")

cal_query_router = APIRouter(prefix="/titanic/cal", tags=["/titanic/cal"])


@cal_query_router.get("/calculate", response_model=TitanicStatsResponse)
async def calculate_survival_stats(
    use_case: CaledonUseCase = Depends(get_caledon_use_case),
) -> TitanicStatsResponse:
    log.info("  ① Inbound Adapter  │ cal_query_router       │ GET /calculate")
    try:
        result = await use_case.calculate_stats()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        log.error("  ✗ Cal READ 실패 — %s", exc)
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return stats_to_response(result)
