from fastapi import APIRouter, Depends

from titanic_m_learning.adapter.inbound.api.dependencies import get_isador_use_case
from titanic_m_learning.adapter.inbound.api.schemas.isador_query_schema import IsadorIntroduceResponse
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.dtos.isador_dto import IsadorIntroduceQuery

isador_query_router = APIRouter(prefix="/titanic/isador", tags=["/titanic/isador"])


@isador_query_router.get("/myself", response_model=IsadorIntroduceResponse)
async def introduce_myself(
    use_case: IsadorUseCase = Depends(get_isador_use_case),
) -> IsadorIntroduceResponse:
    result = await use_case.introduce_myself(IsadorIntroduceQuery(id=8, name='Isidor Straus'))
    return IsadorIntroduceResponse(id=result.id, name=result.name, message=result.message)
