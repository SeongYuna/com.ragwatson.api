from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_rose_use_case
from titanic_m_learning.adapter.inbound.api.mappers.rose_query_mapper import dataset_info_to_response
from titanic_m_learning.adapter.inbound.api.schemas.rose_query_schema import RoseReadDatasetInfoResponse
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.adapter.inbound.api.schemas.rose_query_schema import RoseIntroduceResponse
from titanic_m_learning.app.dtos.rose_dto import RoseIntroduceQuery

rose_query_router = APIRouter(prefix="/titanic/rose", tags=["/titanic/rose"])


@rose_query_router.get("/info", response_model=RoseReadDatasetInfoResponse)
async def get_dataset_info(
    use_case: RoseUseCase = Depends(get_rose_use_case),
) -> RoseReadDatasetInfoResponse:
    try:
        result = await use_case.get_dataset_info()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return dataset_info_to_response(result)

@rose_query_router.get("/myself", response_model=RoseIntroduceResponse)
async def introduce_myself(
    use_case: RoseUseCase = Depends(get_rose_use_case),
) -> RoseIntroduceResponse:
    result = await use_case.introduce_myself(RoseIntroduceQuery(id=12, name='Rose DeWitt Bukater'))
    return RoseIntroduceResponse(id=result.id, name=result.name, message=result.message)

