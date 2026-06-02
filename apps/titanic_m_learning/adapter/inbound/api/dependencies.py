from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic_m_learning.adapter.outbound.pg.james_cmd_pg_repository import JamesCmdPgRepository
from titanic_m_learning.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.use_cases.andrew_query import AndrewQuery
from titanic_m_learning.app.use_cases.caledon_query import CaledonQuery
from titanic_m_learning.app.use_cases.hartley_query import HartleyQuery
from titanic_m_learning.app.use_cases.isador_query import IsadorQuery
from titanic_m_learning.app.use_cases.jack_query import JackQuery
from titanic_m_learning.app.use_cases.james_cmd_interactor import JamesCmdInteractor
from titanic_m_learning.app.use_cases.rose_query import RoseQuery
from titanic_m_learning.app.use_cases.ruth_query import RuthQuery
from titanic_m_learning.app.use_cases.smith_query import SmithQuery
from titanic_m_learning.app.use_cases.walter_query import WalterQuery


def get_james_cmd_use_case(db: AsyncSession = Depends(get_db)) -> JamesCmdUseCase:
    return JamesCmdInteractor(repository=JamesCmdPgRepository(db))


def get_walter_use_case(db: AsyncSession = Depends(get_db)) -> WalterUseCase:
    return WalterQuery(repository=WalterPgRepository(db))

def get_andrew_use_case() -> AndrewUseCase:
    return AndrewQuery()


def get_caledon_use_case() -> CaledonUseCase:
    return CaledonQuery()


def get_jack_use_case() -> JackUseCase:
    return JackQuery()


def get_rose_use_case() -> RoseUseCase:
    return RoseQuery()


def get_ruth_use_case() -> RuthUseCase:
    return RuthQuery()


def get_smith_use_case() -> SmithUseCase:
    return SmithQuery()


def get_isador_use_case() -> IsadorUseCase:
    return IsadorQuery()


def get_hartley_use_case() -> HartleyUseCase:
    return HartleyQuery()

