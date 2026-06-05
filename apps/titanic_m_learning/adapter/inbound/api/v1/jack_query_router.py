from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_jack_use_case
from titanic_m_learning.adapter.inbound.api.mappers.walter_query_mapper import passenger_to_response
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicPassengerResponse
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase

jack_query_router = APIRouter(prefix="/titanic/jack", tags=["/titanic/jack"])


@jack_query_router.get("/passenger/{passenger_id}", response_model=TitanicPassengerResponse)
async def get_passenger_by_id(
    passenger_id: str,
    use_case: JackUseCase = Depends(get_jack_use_case),
) -> TitanicPassengerResponse:
    try:
        passenger = await use_case.find_by_id(passenger_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return passenger_to_response(passenger)
