from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_walter_use_case
from titanic_m_learning.adapter.inbound.api.mappers.walter_query_mapper import (
    table_result_to_responses,
)
from titanic_m_learning.adapter.inbound.api.schemas.walter_query_schema import (
    WalterReadPassengerResponse,
)
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.adapter.inbound.api.schemas.walter_query_schema import WalterIntroduceResponse
from titanic_m_learning.app.dtos.walter_dto import WalterIntroduceQuery

walter_query_router = APIRouter(prefix="/titanic/walter", tags=["/titanic/walter"])


@walter_query_router.get("/table", response_model=list[WalterReadPassengerResponse])
async def get_titanic_table(
    use_case: WalterUseCase = Depends(get_walter_use_case),
) -> list[WalterReadPassengerResponse]:
    try:
        result = await use_case.find_all()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc

    return table_result_to_responses(result)

@walter_query_router.get("/myself", response_model=WalterIntroduceResponse)
async def introduce_myself(
    use_case: WalterUseCase = Depends(get_walter_use_case),
) -> WalterIntroduceResponse:
    result = await use_case.introduce_myself(WalterIntroduceQuery(id=1, name='Walter'))
    return WalterIntroduceResponse(id=result.id, name=result.name, message=result.message)

