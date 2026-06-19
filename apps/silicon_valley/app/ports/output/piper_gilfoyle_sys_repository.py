from abc import ABC, abstractmethod

from silicon_valley.app.dtos.piper_gilfoyle_sys_dto import (
    PiperGilfoyleSysIntroduceQuery,
    PiperGilfoyleSysIntroduceResult,
)


class PiperGilfoyleSysRepository(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: PiperGilfoyleSysIntroduceQuery
    ) -> PiperGilfoyleSysIntroduceResult:
        ...
