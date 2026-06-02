import logging

from titanic_m_learning.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRequest
from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import (
    TitanicPassengerResponse,
    TitanicUploadResponse,
    TitanicStatsResponse,
    TitanicDatasetInfoResponse,
    TitanicColumnResponse,
)
from titanic_m_learning.app.dtos.upload_result import UploadResult
from titanic_m_learning.app.dtos.stats_result import StatsResult
from titanic_m_learning.app.dtos.dataset_info_result import DatasetInfoResult
from titanic_m_learning.domain.entities.titanic import TitanicPassenger

def request_to_passenger(req: TitanicPassengerRequest) -> TitanicPassenger:
    return TitanicPassenger.create(
        passenger_id=req.passenger_id,
        survived=req.survived,
        pclass=req.pclass,
        name=req.name,
        sex=req.gender,
        age=req.age,
        sib_sp=req.sib_sp,
        parch=req.parch,
        ticket=req.ticket,
        fare=req.fare,
        cabin=req.cabin,
        embarked=req.embarked,
    )


def requests_to_passengers(requests: list[TitanicPassengerRequest]) -> list[TitanicPassenger]:
    passengers = [request_to_passenger(req) for req in requests]
    sample = passengers[0] if passengers else None
    if sample:
        log.info(
            "  ② Inbound Mapper   │ titanic_mapper       │ API DTO → Domain │ %d건 · 샘플 id=%s gender=%d",
            len(passengers),
            sample.passenger_id,
            sample.gender.value,
        )
    return passengers


def passenger_to_response(passenger: TitanicPassenger) -> TitanicPassengerResponse:
    return TitanicPassengerResponse(
        passenger_id=passenger.passenger_id,
        survived=passenger.survived,
        pclass=passenger.pclass,
        name=passenger.name,
        gender=passenger.gender.value,
        age=passenger.age,
        sib_sp=passenger.sib_sp,
        parch=passenger.parch,
        ticket=passenger.ticket,
        fare=passenger.fare,
        cabin=passenger.cabin,
        embarked=passenger.embarked,
    )


def passengers_to_responses(
    passengers: list[TitanicPassenger],
) -> list[TitanicPassengerResponse]:
    responses = [passenger_to_response(p) for p in passengers]
    log = logging.getLogger("titanic.read")
    if responses:
        log.info(
            "  ⑥ Inbound Mapper   │ titanic_mapper       │ Domain → API   │ %d건",
            len(responses),
        )
    return responses


def upload_result_to_response(result: UploadResult) -> TitanicUploadResponse:
    return TitanicUploadResponse(count=result.count)


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

