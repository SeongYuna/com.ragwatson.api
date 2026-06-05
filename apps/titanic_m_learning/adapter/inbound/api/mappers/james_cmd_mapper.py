from titanic_m_learning.adapter.inbound.api.schemas.titanic_response import TitanicUploadResponse
from titanic_m_learning.app.dtos.upload_result import UploadResult


def upload_result_to_response(result: UploadResult) -> TitanicUploadResponse:
    return TitanicUploadResponse(count=result.count)
