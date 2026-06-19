from silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    PiperBighettiHrIntroduceQuery,
    PiperBighettiHrIntroduceResult,
)
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import PiperBighettiHrUseCase
from silicon_valley.app.ports.output.piper_bighetti_hr_repository import PiperBighettiHrRepository


class PiperBighettiHrInteractor(PiperBighettiHrUseCase):
    def __init__(self, repository: PiperBighettiHrRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: PiperBighettiHrIntroduceQuery
    ) -> PiperBighettiHrIntroduceResult:
        return await self._repository.introduce_myself(query)
