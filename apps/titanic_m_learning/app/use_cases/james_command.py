import logging

from titanic_m_learning.app.dto.upload_result import UploadResult
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.output.james_repository import JamesRepository
from titanic_m_learning.domain.entities.titanic import TitanicPassenger

log = logging.getLogger("titanic.write")


class JamesCommand(JamesCmdUseCase):
    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def execute(self, passengers: list[TitanicPassenger]) -> UploadResult:
        log.info(
            "  ④ Use Case         │ JamesCommand         │ 저장 시작      │ %d건",
            len(passengers),
        )
        log.info(
            "  ⑤ Output Port      │ JamesRepository      │ save_all() 위임",
        )
        await self._repository.save_all(passengers)
        log.info(
            "  ④ Use Case         │ JamesCommand         │ 저장 완료      │ UploadResult(count=%d)",
            len(passengers),
        )
        return UploadResult(count=len(passengers))
