from titanic_m_learning.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRequest
from titanic_m_learning.app.dtos.upload_result import UploadResult
from titanic_m_learning.app.mappers.james_cmd_mapper import requests_to_commands
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository


class JamesCmdInteractor(JamesCmdUseCase):
    def __init__(self, repository: JamesCmdRepository) -> None:
        self._repository = repository

    async def execute(self, requests: list[TitanicPassengerRequest]) -> UploadResult:
        commands = requests_to_commands(requests)
        await self._repository.save_all(commands)
        return UploadResult(count=len(commands))
