from titanic_m_learning.adapter.outbound.pg.rose_query_pg_repository import RoseQueryPgRepository
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.output.rose_repository import RoseRepository
from titanic_m_learning.app.use_cases.rose_query_interactor import RoseQueryInteractor


def get_rose_use_case() -> RoseUseCase:
    repository: RoseRepository = RoseQueryPgRepository()
    return RoseQueryInteractor(repository=repository)
