from silicon_valley.app.dtos.piper_dinesh_dash_dto import (
    PiperDineshDashIntroduceQuery,
    PiperDineshDashIntroduceResult,
)
from silicon_valley.app.ports.input.piper_dinesh_dash_use_case import PiperDineshDashUseCase
from silicon_valley.app.ports.output.piper_dinesh_dash_repository import PiperDineshDashRepository


class PiperDineshDashInteractor(PiperDineshDashUseCase):
    def __init__(self, repository: PiperDineshDashRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: PiperDineshDashIntroduceQuery
    ) -> PiperDineshDashIntroduceResult:
        return await self._repository.introduce_myself(query)
