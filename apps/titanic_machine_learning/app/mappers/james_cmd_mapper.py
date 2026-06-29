from titanic_machine_learning.adapter.inbound.api.schemas.james_cmd_schema import JamesWritePassengerRequest
from titanic_machine_learning.app.dtos.james_cmd_dto import (
    BookingCommand,
    JamesPassengerCommand,
    PersonCommand,
)


def request_to_command(req: JamesWritePassengerRequest) -> JamesPassengerCommand:
    return JamesPassengerCommand(
        person=PersonCommand(
            passenger_id=req.passenger_id,
            name=req.name,
            gender=req.gender,
            age=req.age,
            sib_sp=req.sib_sp,
            parch=req.parch,
            survived=req.survived,
        ),
        booking=BookingCommand(
            pclass=req.pclass,
            ticket=req.ticket,
            fare=req.fare,
            cabin=req.cabin,
            embarked=req.embarked,
        ),
    )


def requests_to_commands(
    requests: list[JamesWritePassengerRequest],
) -> list[JamesPassengerCommand]:
    return [request_to_command(req) for req in requests]
