from titanic_m_learning.app.dtos.james_cmd_dto import (
    JamesPassengerCommand,
    JamesUploadResult,
    JamesIntroduceQuery,
    JamesIntroduceResult,
)
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.output.james_cmd_port import JamesCmdPort


class JamesCmdInteractor(JamesCmdUseCase):
    def __init__(self, repository: JamesCmdPort) -> None:
        self._repository = repository

    async def execute(self, commands: list[JamesPassengerCommand]) -> JamesUploadResult:
        await self._repository.save_all(commands)
        return JamesUploadResult(count=len(commands))

    async def introduce_myself(self, query: JamesIntroduceQuery) -> JamesIntroduceResult:
        return await self._repository.introduce_myself(query)
