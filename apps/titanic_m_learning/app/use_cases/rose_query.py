from titanic_m_learning.app.dtos.dataset_info_result import DatasetInfoResult
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase


class RoseQuery(RoseUseCase):
    async def get_dataset_info(self) -> DatasetInfoResult:
        raise NotImplementedError("Rose 데이터셋 정보 조회는 아직 구현되지 않았습니다.")
