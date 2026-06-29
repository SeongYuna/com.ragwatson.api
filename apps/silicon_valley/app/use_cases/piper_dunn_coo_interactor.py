from silicon_valley.app.dtos.piper_dunn_coo_dto import (
    PiperDunnCooIntroduceQuery,
    PiperDunnCooIntroduceResult,
)
from silicon_valley.app.ports.input.piper_dunn_coo_use_case import PiperDunnCooUseCase
from silicon_valley.app.ports.output.piper_dunn_coo_port import PiperDunnCooRepository


class PiperDunnCooInteractor(PiperDunnCooUseCase):
    def __init__(self, repository: PiperDunnCooRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: PiperDunnCooIntroduceQuery
    ) -> PiperDunnCooIntroduceResult:
        return await self._repository.introduce_myself(query)
