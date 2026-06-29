from titanic_machine_learning.adapter.inbound.api.schemas.rose_query_schema import (
    RoseReadColumnResponse,
    RoseReadDatasetInfoResponse,
)
from titanic_machine_learning.app.dtos.rose_dto import RoseDatasetInfoResult


def dataset_info_to_response(result: RoseDatasetInfoResult) -> RoseReadDatasetInfoResponse:
    return RoseReadDatasetInfoResponse(
        columns=[
            RoseReadColumnResponse(
                name=column.name,
                description=column.description,
                role=column.role,
            )
            for column in result.columns
        ],
    )
