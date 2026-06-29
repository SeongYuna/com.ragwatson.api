from fastapi import Depends

from titanic_machine_learning.adapter.outbound.repositories.rose_query_repository import RoseQueryRepository
from titanic_machine_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_machine_learning.app.ports.output.rose_port import RosePort
from titanic_machine_learning.app.use_cases.rose_query_interactor import RoseQueryInteractor


def get_rose_repository() -> RosePort:
    return RoseQueryRepository()


def get_rose_use_case(
    repository: RosePort = Depends(get_rose_repository)
) -> RoseUseCase:
    return RoseQueryInteractor(repository=repository)
