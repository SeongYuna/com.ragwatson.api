from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_sys_query_schema import PiperGilfoyleSysIntroduceResponse
from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import PiperGilfoyleSysIntroduceResult


def result_to_response(result: PiperGilfoyleSysIntroduceResult) -> PiperGilfoyleSysIntroduceResponse:
    return PiperGilfoyleSysIntroduceResponse(id=result.id, name=result.name, message=result.message)
