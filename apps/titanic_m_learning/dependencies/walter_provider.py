"""
Walter Query 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(WalterPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(WalterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from core.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from titanic_m_learning.adapter.outbound.pg.walter_pg_repository import WalterPgRepository
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository
from titanic_m_learning.app.use_cases.walter_query_interactor import WalterQueryInteractor


def get_walter_use_case(
    db: AsyncSession = Depends(get_db),
) -> WalterUseCase:
    repository: WalterRepository = WalterPgRepository(db=db)
    return WalterQueryInteractor(repository=repository)
