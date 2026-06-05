from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import (
    TitanicColumnResponse,
    TitanicDatasetInfoResponse,
    TitanicStatsResponse,
)
from titanic_m_learning.app.dtos.dataset_info_result import DatasetInfoResult
from titanic_m_learning.app.dtos.stats_result import StatsResult


def stats_to_response(result: StatsResult) -> TitanicStatsResponse:
    return TitanicStatsResponse(
        total=result.total,
        survived=result.survived,
        deceased=result.deceased,
        survival_rate=result.survival_rate,
    )


def dataset_info_to_response(result: DatasetInfoResult) -> TitanicDatasetInfoResponse:
    return TitanicDatasetInfoResponse(
        columns=[
            TitanicColumnResponse(
                name=column.name,
                description=column.description,
                role=column.role,
            )
            for column in result.columns
        ],
    )
