from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_bighetti_hr_dto import (
    PiperBighettiHrIntroduceQuery,
    PiperBighettiHrIntroduceResult,
)


class PiperBighettiHrRepository(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: PiperBighettiHrIntroduceQuery
    ) -> PiperBighettiHrIntroduceResult:
        ...
