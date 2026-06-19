from silicon_valley.adapter.inbound.api.schemas.piper_dinesh_dash_query_schema import PiperDineshDashIntroduceResponse
from silicon_valley.app.dtos.piper_dinesh_dash_dto import PiperDineshDashIntroduceResult


def result_to_response(result: PiperDineshDashIntroduceResult) -> PiperDineshDashIntroduceResponse:
    return PiperDineshDashIntroduceResponse(id=result.id, name=result.name, message=result.message)
