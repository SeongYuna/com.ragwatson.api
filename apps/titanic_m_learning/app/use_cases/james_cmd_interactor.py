from titanic_m_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesWritePassengerRequest
from titanic_m_learning.app.dtos.james_cmd_dto import JamesUploadResult
from titanic_m_learning.app.mappers.james_cmd_mapper import requests_to_commands
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository
from titanic_m_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesIntroduceResponse, JamesIntroduceSchema
from titanic_m_learning.app.dtos.james_cmd_dto import JamesIntroduceQuery


class JamesCmdInteractor(JamesCmdUseCase):
    def __init__(self, repository: JamesCmdRepository) -> None:
        self._repository = repository

    async def execute(self, requests: list[JamesWritePassengerRequest]) -> JamesUploadResult:
        commands = requests_to_commands(requests)
        await self._repository.save_all(commands)
        return JamesUploadResult(count=len(commands))
    async def introduce_myself(self, schema: JamesIntroduceSchema) -> JamesIntroduceResponse:
        result = await self._repository.introduce_myself(
            JamesIntroduceQuery(id=schema.id, name=schema.name)
        )
        return JamesIntroduceResponse(
            id=result.id,
            name=result.name,
            message=result.message,
        )

