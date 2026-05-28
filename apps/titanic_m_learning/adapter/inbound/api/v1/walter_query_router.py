import logging

from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_walter_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_mapper import passengers_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase

log = logging.getLogger("titanic.read")

walter_query_router = APIRouter(prefix="/titanic/walter", tags=["/titanic/walter"])


@walter_query_router.get("/table", response_model=list[TitanicPassengerResponse])
async def get_titanic_table(
    use_case: WalterUseCase = Depends(get_walter_use_case),
) -> list[TitanicPassengerResponse]:
    log.info("")
    log.info("╔══════════════════════════════════════════════════╗")
    log.info("║  TITANIC READ — 목록 조회 흐름 시작              ║")
    log.info("╚══════════════════════════════════════════════════╝")
    log.info(
        "  ① Inbound Adapter  │ walter_query_router  │ GET /table",
    )
    log.info(
        "  ② Input Port       │ WalterUseCase        │ find_all() 호출",
    )

    try:
        passengers = await use_case.find_all()
    except Exception as exc:
        log.error("  ✗ READ 실패 — %s", exc)
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc

    result = passengers_to_responses(passengers)
    log.info(
        "  ① Inbound Adapter  │ walter_query_router  │ API 응답       │ %d건",
        len(result),
    )
    log.info("╔══════════════════════════════════════════════════╗")
    log.info("║  TITANIC READ — OK                               ║")
    log.info("╚══════════════════════════════════════════════════╝")
    log.info("")
    return result
