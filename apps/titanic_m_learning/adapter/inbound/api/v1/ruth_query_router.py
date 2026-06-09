from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_ruth_use_case
from titanic_m_learning.adapter.inbound.api.mappers.ruth_query_mapper import queries_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthReadPassengerResponse
from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_m_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthIntroduceResponse, RuthIntroduceSchema

ruth_query_router = APIRouter(prefix="/titanic/ruth", tags=["/titanic/ruth"])


@ruth_query_router.get("/first-class", response_model=list[RuthReadPassengerResponse])
async def get_first_class_passengers(
    use_case: RuthUseCase = Depends(get_ruth_use_case),
) -> list[RuthReadPassengerResponse]:
    try:
        queries = await use_case.find_first_class()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return queries_to_responses(queries)

@ruth_query_router.get("/myself", response_model=RuthIntroduceResponse)
async def introduce_myself(
    use_case: RuthUseCase = Depends(get_ruth_use_case),
) -> RuthIntroduceResponse:
    return await use_case.introduce_myself(
        RuthIntroduceSchema(
            id=6,
            name='Ruth',
        )
    )

