from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import SmithReadStatsResponse
from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import (
    SmithChatRequest,
    SmithChatResponse,
)
from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult, SmithChatMessageDto, SmithChatQuery, SmithChatResult


def stats_to_response(result: SmithStatsResult) -> SmithReadStatsResponse:
    return SmithReadStatsResponse(
        total=result.total,
        survived=result.survived,
        deceased=result.deceased,
        survival_rate=result.survival_rate,
    )


def chat_request_to_query(body: SmithChatRequest) -> SmithChatQuery:
    return SmithChatQuery(
        messages=tuple(
            SmithChatMessageDto(role=message.role, content=message.content)
            for message in body.messages
        ),
        model=body.model,
    )


def chat_result_to_response(result: SmithChatResult) -> SmithChatResponse:
    return SmithChatResponse(reply=result.reply)
