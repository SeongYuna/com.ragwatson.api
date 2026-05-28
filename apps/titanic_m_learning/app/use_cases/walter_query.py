import logging

from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.output.walter_repository import WalterRepository
from titanic_m_learning.domain.entities.titanic import TitanicPassenger

log = logging.getLogger("titanic.read")


class WalterQuery(WalterUseCase):
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def find_all(self) -> list[TitanicPassenger]:
        log.info(
            "  ③ Use Case         │ WalterQuery          │ 조회 시작",
        )
        log.info(
            "  ④ Output Port      │ WalterRepository     │ find_all() 위임",
        )
        rows = await self._repository.find_all()
        log.info(
            "  ③ Use Case         │ WalterQuery          │ Domain %d건 반환",
            len(rows),
        )
        return rows
