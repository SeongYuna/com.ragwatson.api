from titanic_machine_learning.app.ports.input.molly_use_case import MollyUseCase
from titanic_machine_learning.app.ports.output.molly_port import MollyPort
from titanic_machine_learning.app.dtos.molly_dto import MollyIntroduceQuery, MollyIntroduceResult


class MollyQueryInteractor(MollyUseCase):
    def __init__(self, repository: MollyPort) -> None:
        self._repository = repository

    async def introduce_myself(self, query: MollyIntroduceQuery) -> MollyIntroduceResult:
        return await self._repository.introduce_myself(query)
