from fastapi import APIRouter, Depends, HTTPException, Query

from titanic_m_learning.adapter.inbound.api.dependencies import get_andrew_use_case
from titanic_m_learning.adapter.inbound.api.mappers.walter_query_mapper import passengers_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase

andrew_query_router = APIRouter(prefix="/titanic/andrew", tags=["/titanic/andrew"])


@andrew_query_router.get("/table", response_model=list[TitanicPassengerResponse])
async def get_titanic_table_page(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    use_case: AndrewUseCase = Depends(get_andrew_use_case),
) -> list[TitanicPassengerResponse]:
    try:
        passengers = await use_case.find_page(skip=skip, limit=limit)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return passengers_to_responses(passengers)
