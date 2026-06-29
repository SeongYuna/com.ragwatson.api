from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import (
    PiperGilfoyleSysIntroduceQuery,
    PiperGilfoyleSysIntroduceResult,
)
from silicon_valley.app.ports.input.piper_gilfoyle_sys_use_case import PiperGilfoyleSysUseCase
from silicon_valley.app.ports.output.piper_gilfoyle_sys_port import PiperGilfoyleSysRepository


class PiperGilfoyleSysInteractor(PiperGilfoyleSysUseCase):
    def __init__(self, repository: PiperGilfoyleSysRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: PiperGilfoyleSysIntroduceQuery
    ) -> PiperGilfoyleSysIntroduceResult:
        return await self._repository.introduce_myself(query)
