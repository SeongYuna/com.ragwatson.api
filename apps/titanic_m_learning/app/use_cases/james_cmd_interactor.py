import logging

from titanic_m_learning.adapter.inbound.api.schemas.titanic_request import TitanicPassengerRequest
from titanic_m_learning.app.dtos.upload_result import UploadResult
from titanic_m_learning.app.mappers.james_cmd_mapper import requests_to_commands
from titanic_m_learning.app.ports.input.james_cmd_use_case import JamesCmdUseCase
from titanic_m_learning.app.ports.output.james_cmd_repository import JamesCmdRepository

log = logging.getLogger("titanic.write")


class JamesCmdInteractor(JamesCmdUseCase):
    def __init__(self, repository: JamesCmdRepository) -> None:
        self._repository = repository

    async def execute(self, requests: list[TitanicPassengerRequest]) -> UploadResult:
        log.info(
            "  ③ Input Port       │ JamesCmdUseCase          │ execute()      │ Request %d건",
            len(requests),
        )
        commands = requests_to_commands(requests)
        sample = commands[0] if commands else None
        if sample:
            log.info(
                "  ④ Use Case         │ JamesCmdInteractor         │ Request → Command │ %d건 · 샘플 id=%s pclass=%s",
                len(commands),
                sample.person.passenger_id,
                sample.booking.pclass,
            )
        log.info("  ④ Use Case         │ JamesCmdInteractor         │ Command 상위 5행")
        for index, command in enumerate(commands[:5], start=1):
            person = command.person
            booking = command.booking
            log.info("    #%d ─ PersonCommand", index)
            log.info(
                "         id=%s name=%s gender=%s age=%s sib_sp=%s parch=%s survived=%s",
                person.passenger_id,
                person.name,
                person.gender,
                person.age,
                person.sib_sp,
                person.parch,
                person.survived,
            )
            log.info("    #%d ─ BookingCommand", index)
            log.info(
                "         pclass=%s ticket=%s fare=%s cabin=%s embarked=%s",
                booking.pclass,
                booking.ticket,
                booking.fare,
                booking.cabin,
                booking.embarked,
            )
        log.info(
            "  ⑤ Output Port      │ JamesCmdRepository         │ save_all()     │ Command %d건",
            len(commands),
        )
        await self._repository.save_all(commands)
        log.info(
            "  ④ Use Case         │ JamesCmdInteractor         │ 저장 완료      │ UploadResult(count=%d)",
            len(commands),
        )
        return UploadResult(count=len(commands))
