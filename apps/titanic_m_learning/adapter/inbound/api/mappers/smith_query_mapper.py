from titanic_m_learning.adapter.inbound.api.schemas.smith_query_schema import SmithReadStatsResponse
from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult


def stats_to_response(result: SmithStatsResult) -> SmithReadStatsResponse:
    return SmithReadStatsResponse(
        total=result.total,
        survived=result.survived,
        deceased=result.deceased,
        survival_rate=result.survival_rate,
    )
