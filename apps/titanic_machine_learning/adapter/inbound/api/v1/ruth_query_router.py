from fastapi import APIRouter, Depends

from titanic_machine_learning.adapter.inbound.api.dependencies import get_ruth_use_case
from titanic_machine_learning.adapter.inbound.api.schemas.ruth_query_schema import RuthIntroduceResponse
from titanic_machine_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_machine_learning.app.dtos.ruth_dto import RuthIntroduceQuery

ruth_query_router = APIRouter(prefix="/titanic/ruth", tags=["/titanic/ruth"])


@ruth_query_router.get("/myself", response_model=RuthIntroduceResponse)
async def introduce_myself(
    use_case: RuthUseCase = Depends(get_ruth_use_case),
) -> RuthIntroduceResponse:
    result = await use_case.introduce_myself(RuthIntroduceQuery(id=6, name='Ruth'))
    return RuthIntroduceResponse(id=result.id, name=result.name, message=result.message)
