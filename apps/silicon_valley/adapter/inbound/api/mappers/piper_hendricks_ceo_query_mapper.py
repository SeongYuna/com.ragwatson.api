from silicon_valley.adapter.inbound.api.schemas.piper_hendricks_ceo_query_schema import PiperHendricksCeoIntroduceResponse
from silicon_valley.app.dtos.piper_hendricks_ceo_dto import PiperHendricksCeoIntroduceResult


def result_to_response(result: PiperHendricksCeoIntroduceResult) -> PiperHendricksCeoIntroduceResponse:
    return PiperHendricksCeoIntroduceResponse(id=result.id, name=result.name, message=result.message)
