from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_isador_use_case
from titanic_m_learning.adapter.inbound.api.mappers.walter_query_mapper import passengers_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase

isador_query_router = APIRouter(prefix="/titanic/isador", tags=["/titanic/isador"])


@isador_query_router.get("/families", response_model=list[TitanicPassengerResponse])
async def get_family_passengers(
    use_case: IsadorUseCase = Depends(get_isador_use_case),
) -> list[TitanicPassengerResponse]:
    try:
        passengers = await use_case.find_families()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return passengers_to_responses(passengers)
