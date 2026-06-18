from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated

from titanic_m_learning.adapter.inbound.api.dependencies import get_smith_use_case
from titanic_m_learning.adapter.inbound.api.mappers.smith_query_mapper import stats_to_response
from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import (
    SmithChatRequest,
    SmithChatResponse,
    SmithIntroduceResponse,
    SmithReadStatsResponse,
)
from titanic_m_learning.app.dtos.smith_dto import (
    SmithChatMessageDto,
    SmithChatQuery,
    SmithIntroduceQuery,
)
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase

smith_query_router = APIRouter(prefix="/titanic/smith", tags=["/titanic/smith"])


@smith_query_router.get("/summary", response_model=SmithReadStatsResponse)
async def get_passenger_summary(
    use_case: SmithUseCase = Depends(get_smith_use_case),
) -> SmithReadStatsResponse:
    try:
        result = await use_case.get_summary()
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"서버 오류: {exc}") from exc
    return stats_to_response(result)


@smith_query_router.get("/myself", response_model=SmithIntroduceResponse)
async def introduce_myself(
    use_case: SmithUseCase = Depends(get_smith_use_case),
) -> SmithIntroduceResponse:
    result = await use_case.introduce_myself(
        SmithIntroduceQuery(id=5, name="에드워드 스미스 (Edward Smith)")
    )
    return SmithIntroduceResponse(id=result.id, name=result.name, message=result.message)


@smith_query_router.post("/chat", response_model=SmithChatResponse)
async def chat(
    schema: Annotated[SmithChatRequest, Body()],
    smith: SmithUseCase = Depends(get_smith_use_case),
) -> SmithChatResponse:
    try:
        query = SmithChatQuery(
            messages=tuple(
                SmithChatMessageDto(role=m.role, content=m.content)
                for m in schema.messages
            ),
            model=schema.model,
        )
        result = await smith.chat(query)
        return SmithChatResponse(reply=result.reply)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
