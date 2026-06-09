from fastapi import APIRouter, Depends, HTTPException, Query

from titanic_m_learning.adapter.inbound.api.dependencies import get_andrew_use_case
from titanic_m_learning.adapter.inbound.api.mappers.andrew_query_mapper import queries_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.andrew_query_schema import AndrewReadPassengerResponse
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.adapter.inbound.api.schemas.andrew_query_schema import AndrewIntroduceResponse, AndrewIntroduceSchema

andrew_query_router = APIRouter(prefix="/titanic/andrew", tags=["/titanic/andrew"])


@andrew_query_router.get("/table", response_model=list[AndrewReadPassengerResponse])
async def get_titanic_table_page(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    use_case: AndrewUseCase = Depends(get_andrew_use_case),
) -> list[AndrewReadPassengerResponse]:
    try:
        result = await use_case.find_page(skip=skip, limit=limit)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return queries_to_responses(result.passengers)

@andrew_query_router.get("/myself", response_model=AndrewIntroduceResponse)
async def introduce_myself(
    use_case: AndrewUseCase = Depends(get_andrew_use_case),
) -> AndrewIntroduceResponse:
    return await use_case.introduce_myself(
        AndrewIntroduceSchema(
            id=2,
            name='토마스 앤드류스 (Thomas Andrews)',
        )
    )

