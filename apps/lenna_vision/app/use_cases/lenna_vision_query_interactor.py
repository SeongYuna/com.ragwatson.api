from lenna_vision.app.ports.input.lenna_vision_use_case import LennaVisionUseCase
from lenna_vision.app.ports.output.lenna_vision_port import LennaVisionPort
from lenna_vision.app.dtos.lenna_vision_dto import (
    LennaImageUploadCommand,
    LennaImageUploadResult,
    LennaVisionIntroduceQuery,
    LennaVisionIntroduceResult,
)


class LennaVisionQueryInteractor(LennaVisionUseCase):
    def __init__(self, repository: LennaVisionPort) -> None:
        self._repository = repository

    async def introduce_myself(self, query: LennaVisionIntroduceQuery) -> LennaVisionIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def upload_image(self, command: LennaImageUploadCommand) -> LennaImageUploadResult:
        return await self._repository.save_image(command)
