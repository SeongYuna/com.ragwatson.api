import logging

from fastapi import APIRouter, Depends, HTTPException

from titanic_m_learning.adapter.inbound.api.dependencies import get_rose_use_case
from titanic_m_learning.adapter.inbound.api.mappers.titanic_mapper import dataset_info_to_response
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicDatasetInfoResponse
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase

log = logging.getLogger("titanic.read")

rose_query_router = APIRouter(prefix="/titanic/rose", tags=["/titanic/rose"])


@rose_query_router.get("/info", response_model=TitanicDatasetInfoResponse)
async def get_dataset_info(
    use_case: RoseUseCase = Depends(get_rose_use_case),
) -> TitanicDatasetInfoResponse:
    log.info("  ① Inbound Adapter  │ rose_query_router      │ GET /info")
    try:
        result = await use_case.get_dataset_info()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        log.error("  ✗ Rose READ 실패 — %s", exc)
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return dataset_info_to_response(result)
