from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from titanic_m_learning.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic_m_learning.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.use_cases.james_command import JamesCommand
from titanic_m_learning.app.use_cases.walter_query import WalterQuery


def get_james_cmd_use_case(db: AsyncSession = Depends(get_db)) -> JamesCmdUseCase:
    return JamesCommand(repository=JamesPgRepository(db))


def get_walter_use_case(db: AsyncSession = Depends(get_db)) -> WalterUseCase:
    return WalterQuery(repository=WalterPgRepository(db))
