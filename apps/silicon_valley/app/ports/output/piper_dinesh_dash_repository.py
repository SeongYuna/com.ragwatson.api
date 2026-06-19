from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_dinesh_dash_dto import (
    PiperDineshDashIntroduceQuery,
    PiperDineshDashIntroduceResult,
)


class PiperDineshDashRepository(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: PiperDineshDashIntroduceQuery
    ) -> PiperDineshDashIntroduceResult:
        ...
