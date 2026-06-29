from titanic_machine_learning.adapter.inbound.api.schemas.caledon_query_schema import CaledonReadStatsResponse
from titanic_machine_learning.app.dtos.caledon_dto import CaledonStatsResult


def stats_to_response(result: CaledonStatsResult) -> CaledonReadStatsResponse:
    return CaledonReadStatsResponse(
        total=result.total,
        survived=result.survived,
        deceased=result.deceased,
        survival_rate=result.survival_rate,
    )
