from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_hendricks_ceo_dto import (
    PiperHendricksCeoIntroduceQuery,
    PiperHendricksCeoIntroduceResult,
)


class PiperHendricksCeoUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: PiperHendricksCeoIntroduceQuery
    ) -> PiperHendricksCeoIntroduceResult:
        ...
