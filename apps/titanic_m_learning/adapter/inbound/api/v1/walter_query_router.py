from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_walter_use_case
from titanic_m_learning.adapter.inbound.api.mappers.walter_query_mapper import (
    table_result_to_responses,
)
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase

walter_query_router = APIRouter(prefix="/titanic/walter", tags=["/titanic/walter"])


@walter_query_router.get("/table", response_model=list[TitanicPassengerResponse])
async def get_titanic_table(
    use_case: WalterUseCase = Depends(get_walter_use_case),
) -> list[TitanicPassengerResponse]:
    try:
        result = await use_case.find_all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc

    return table_result_to_responses(result)
