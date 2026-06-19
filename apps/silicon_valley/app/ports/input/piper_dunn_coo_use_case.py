from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_dunn_coo_dto import (
    PiperDunnCooIntroduceQuery,
    PiperDunnCooIntroduceResult,
)


class PiperDunnCooUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: PiperDunnCooIntroduceQuery
    ) -> PiperDunnCooIntroduceResult:
        ...
