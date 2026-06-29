from fastapi import APIRouter, Depends, HTTPException

from titanic_machine_learning.adapter.inbound.api.dependencies import get_jack_use_case
from titanic_machine_learning.adapter.inbound.api.mappers.jack_query_mapper import query_to_response
from titanic_machine_learning.adapter.inbound.api.schemas.jack_query_schema import JackReadPassengerResponse
from titanic_machine_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_machine_learning.adapter.inbound.api.schemas.jack_query_schema import JackIntroduceResponse
from titanic_machine_learning.app.dtos.jack_dto import JackIntroduceQuery

jack_query_router = APIRouter(prefix="/titanic/jack", tags=["/titanic/jack"])


@jack_query_router.get("/passenger/{passenger_id}", response_model=JackReadPassengerResponse)
async def get_passenger_by_id(
    passenger_id: str,
    use_case: JackUseCase = Depends(get_jack_use_case),
) -> JackReadPassengerResponse:
    try:
        query = await use_case.find_by_id(passenger_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return query_to_response(query)

@jack_query_router.get("/myself", response_model=JackIntroduceResponse)
async def introduce_myself(
    use_case: JackUseCase = Depends(get_jack_use_case),
) -> JackIntroduceResponse:
    result = await use_case.introduce_myself(JackIntroduceQuery(id=3, name='Jack Dawson'))
    return JackIntroduceResponse(id=result.id, name=result.name, message=result.message)

