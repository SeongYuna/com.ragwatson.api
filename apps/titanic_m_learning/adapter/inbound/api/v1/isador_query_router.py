from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_isador_use_case
from titanic_m_learning.adapter.inbound.api.mappers.isador_query_mapper import queries_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorReadPassengerResponse
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorIntroduceResponse, IsadorIntroduceSchema

isador_query_router = APIRouter(prefix="/titanic/isador", tags=["/titanic/isador"])


@isador_query_router.get("/families", response_model=list[IsadorReadPassengerResponse])
async def get_family_passengers(
    use_case: IsadorUseCase = Depends(get_isador_use_case),
) -> list[IsadorReadPassengerResponse]:
    try:
        queries = await use_case.find_families()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return queries_to_responses(queries)

@isador_query_router.get("/myself", response_model=IsadorIntroduceResponse)
async def introduce_myself(
    use_case: IsadorUseCase = Depends(get_isador_use_case),
) -> IsadorIntroduceResponse:
    return await use_case.introduce_myself(
        IsadorIntroduceSchema(
            id=8,
            name='Isidor Straus',
        )
    )

