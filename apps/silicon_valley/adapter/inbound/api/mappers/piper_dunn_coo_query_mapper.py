from silicon_valley.adapter.inbound.api.schemas.piper_dunn_coo_query_schema import PiperDunnCooIntroduceResponse
from silicon_valley.app.dtos.piper_dunn_coo_dto import PiperDunnCooIntroduceResult


def result_to_response(result: PiperDunnCooIntroduceResult) -> PiperDunnCooIntroduceResponse:
    return PiperDunnCooIntroduceResponse(id=result.id, name=result.name, message=result.message)
