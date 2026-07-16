"""
Walter Query 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(WalterPort)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(WalterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""

from titanic_machine_learning.adapter.outbound.database import get_titanic_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.adapter.outbound.repositories.walter_repository import WalterRepository
from titanic_machine_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_machine_learning.app.ports.output.walter_port import WalterPort
from titanic_machine_learning.app.use_cases.walter_query_interactor import WalterQueryInteractor


def get_walter_repository(
        db: AsyncSession = Depends(get_titanic_db)
) -> WalterPort:
    return WalterRepository(db=db)


def get_walter_use_case(
    repository: WalterPort = Depends(get_walter_repository)
) -> WalterUseCase:
    return WalterQueryInteractor(repository=repository)
