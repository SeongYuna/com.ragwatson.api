from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_query_schema import PiperBighettiHrIntroduceResponse
from silicon_valley.app.dtos.piper_bighetti_hr_dto import PiperBighettiHrIntroduceResult


def result_to_response(result: PiperBighettiHrIntroduceResult) -> PiperBighettiHrIntroduceResponse:
    return PiperBighettiHrIntroduceResponse(id=result.id, name=result.name, message=result.message)
