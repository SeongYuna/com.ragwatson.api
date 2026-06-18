from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_molly_use_case
from titanic_m_learning.adapter.inbound.api.mappers.molly_query_mapper import result_to_responses
from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyReadNotableSurvivorResponse
from titanic_m_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_m_learning.adapter.inbound.api.schemas.molly_query_schema import MollyIntroduceResponse
from titanic_m_learning.app.dtos.molly_dto import MollyIntroduceQuery

molly_query_router = APIRouter(prefix="/titanic/molly", tags=["/titanic/molly"])


@molly_query_router.get("/notable", response_model=list[MollyReadNotableSurvivorResponse])
async def get_notable_survivors(
    use_case: MollyUseCase = Depends(get_molly_use_case),
) -> list[MollyReadNotableSurvivorResponse]:
    try:
        result = await use_case.find_notable()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return result_to_responses(result)

@molly_query_router.get("/myself", response_model=MollyIntroduceResponse)
async def introduce_myself(
    use_case: MollyUseCase = Depends(get_molly_use_case),
) -> MollyIntroduceResponse:
    result = await use_case.introduce_myself(MollyIntroduceQuery(id=10, name='Margaret Brown'))
    return MollyIntroduceResponse(id=result.id, name=result.name, message=result.message)

