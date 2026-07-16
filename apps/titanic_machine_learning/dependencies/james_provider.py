"""
James CMD 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JamesCmdPort)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JamesCmdUseCase)로 선언한다.
  - 세션은 titanic 전용 get_titanic_db 에서 주입받는다 (AsyncSession, Neon 접속).
"""

from titanic_machine_learning.adapter.outbound.database import get_titanic_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_machine_learning.adapter.outbound.repositories.james_cmd_repository import JamesCmdRepository
from titanic_machine_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_machine_learning.app.ports.output.james_cmd_port import JamesCmdPort
from titanic_machine_learning.app.use_cases.james_cmd_interactor import JamesCmdInteractor


def get_james_cmd_repository(
        db: AsyncSession = Depends(get_titanic_db)
) -> JamesCmdPort:
    return JamesCmdRepository(db=db)


def get_james_cmd_use_case(
    repository: JamesCmdPort = Depends(get_james_cmd_repository)
) -> JamesCmdUseCase:
    return JamesCmdInteractor(repository=repository)
