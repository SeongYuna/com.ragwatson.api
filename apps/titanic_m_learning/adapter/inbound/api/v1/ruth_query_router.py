import logging

from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_ruth_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_mapper import passengers_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase

log = logging.getLogger("titanic.read")

ruth_query_router = APIRouter(prefix="/titanic/ruth", tags=["/titanic/ruth"])


@ruth_query_router.get("/first-class", response_model=list[TitanicPassengerResponse])
async def get_first_class_passengers(
    use_case: RuthUseCase = Depends(get_ruth_use_case),
) -> list[TitanicPassengerResponse]:
    log.info("  ① Inbound Adapter  │ ruth_query_router      │ GET /first-class")
    try:
        passengers = await use_case.find_first_class()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        log.error("  ✗ Ruth READ 실패 — %s", exc)
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return passengers_to_responses(passengers)
