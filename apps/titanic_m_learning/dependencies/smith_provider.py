from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.pg.smith_stats_pg_repository import SmithStatsPgRepository
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.smith_repository import SmithRepository
from titanic_m_learning.app.use_cases.smith_query_interactor import SmithQueryInteractor
from titanic_m_learning.dependencies.andrew_provider import get_andrew_use_case
from titanic_m_learning.dependencies.jack_provider import get_jack_use_case
from titanic_m_learning.dependencies.rose_provider import get_rose_use_case
from titanic_m_learning.dependencies.walter_provider import get_walter_use_case
from titanic_m_learning.dependencies.caledon_provider import get_caledon_use_case
from titanic_m_learning.dependencies.lowe_provider import get_lowe_use_case
from titanic_m_learning.dependencies.hartley_provider import get_hartley_use_case


def get_smith_repository(
        db: AsyncSession = Depends(get_db)
) -> SmithRepository:
    return SmithStatsPgRepository(db=db)


def get_smith_use_case(
    repository: SmithRepository = Depends(get_smith_repository),
    andrew: AndrewUseCase = Depends(get_andrew_use_case),
    jack: JackUseCase = Depends(get_jack_use_case),
    rose: RoseUseCase = Depends(get_rose_use_case),
    walter: WalterUseCase = Depends(get_walter_use_case),
    caledon: CaledonUseCase = Depends(get_caledon_use_case),
    lowe: LoweUseCase = Depends(get_lowe_use_case),
    hartley: HartleyUseCase = Depends(get_hartley_use_case),
) -> SmithUseCase:
    return SmithQueryInteractor(
        repository=repository,
        andrew=andrew,
        jack=jack,
        rose=rose,
        walter=walter,
        caledon=caledon,
        lowe=lowe,
        hartley=hartley,
    )
