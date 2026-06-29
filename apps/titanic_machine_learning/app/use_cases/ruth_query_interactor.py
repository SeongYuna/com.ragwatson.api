from titanic_machine_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_machine_learning.app.ports.output.ruth_port import RuthPort
from titanic_machine_learning.app.dtos.ruth_dto import RuthIntroduceQuery, RuthIntroduceResult


class RuthQueryInteractor(RuthUseCase):
    def __init__(self, repository: RuthPort) -> None:
        self._repository = repository

    async def introduce_myself(self, query: RuthIntroduceQuery) -> RuthIntroduceResult:
        return await self._repository.introduce_myself(query)
