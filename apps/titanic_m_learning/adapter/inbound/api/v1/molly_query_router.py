from fastapi import APIRouter, Depends

from titanic_m_learning.adapter.inbound.api.dependencies import get_molly_use_case
from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyIntroduceResponse
from titanic_m_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery

molly_query_router = APIRouter(prefix="/titanic/molly", tags=["/titanic/molly"])


@molly_query_router.get("/myself", response_model=MollyIntroduceResponse)
async def introduce_myself(
    use_case: MollyUseCase = Depends(get_molly_use_case),
) -> MollyIntroduceResponse:
    result = await use_case.introduce_myself(MollyIntroduceQuery(id=10, name='Margaret Brown'))
    return MollyIntroduceResponse(id=result.id, name=result.name, message=result.message)
