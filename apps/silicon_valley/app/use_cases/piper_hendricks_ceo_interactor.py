from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    PiperHendricksCeoIntroduceQuery,
    PiperHendricksCeoIntroduceResult,
)
from silicon_valley.app.ports.input.piper_hendricks_ceo_use_case import PiperHendricksCeoUseCase
from silicon_valley.app.ports.output.piper_hendricks_ceo_port import PiperHendricksCeoRepository


class PiperHendricksCeoInteractor(PiperHendricksCeoUseCase):
    def __init__(self, repository: PiperHendricksCeoRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: PiperHendricksCeoIntroduceQuery
    ) -> PiperHendricksCeoIntroduceResult:
        return await self._repository.introduce_myself(query)
