import logging

from fastapi import APIRouter, Depends, HTTPException, Query

from titanic_m_learning.adapter.inbound.api.dependencies import get_hartley_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_mapper import passengers_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase

log = logging.getLogger("titanic.read")

hartley_query_router = APIRouter(prefix="/titanic/hartley", tags=["/titanic/hartley"])


@hartley_query_router.get("/sample", response_model=list[TitanicPassengerResponse])
async def get_passenger_sample(
    count: int = Query(10, ge=1, le=100),
    use_case: HartleyUseCase = Depends(get_hartley_use_case),
) -> list[TitanicPassengerResponse]:
    log.info("  ① Inbound Adapter  │ hartley_query_router   │ GET /sample count=%d", count)
    try:
        passengers = await use_case.sample(count=count)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        log.error("  ✗ Hartley READ 실패 — %s", exc)
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return passengers_to_responses(passengers)
