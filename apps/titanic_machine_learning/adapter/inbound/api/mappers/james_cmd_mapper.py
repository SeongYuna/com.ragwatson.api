from titanic_machine_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesWriteUploadResponse
from titanic_machine_learning.app.dtos.james_cmd_dto import JamesUploadResult


def upload_result_to_response(result: JamesUploadResult) -> JamesWriteUploadResponse:
    return JamesWriteUploadResponse(count=result.count)
