from abc import ABC, abstractmethod

from lenna_vision.app.dtos.lenna_vision_dto import (
    LennaImageUploadCommand,
    LennaImageUploadResult,
    LennaVisionIntroduceQuery,
    LennaVisionIntroduceResult,
)


class LennaVisionUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: LennaVisionIntroduceQuery) -> LennaVisionIntroduceResult:
        ...

    @abstractmethod
    async def upload_image(self, command: LennaImageUploadCommand) -> LennaImageUploadResult:
        ...
