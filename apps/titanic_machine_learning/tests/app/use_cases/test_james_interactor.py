import pytest
from unittest.mock import AsyncMock, MagicMock

from titanic_machine_learning.app.use_cases.james_cmd_interactor import JamesCmdInteractor
from titanic_machine_learning.app.dtos.james_cmd_dto import (
    JamesPassengerCommand,
    PersonCommand,
    BookingCommand,
    JamesIntroduceQuery,
    JamesIntroduceResult,
    JamesUploadResult,
)


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JamesIntroduceResult(id=4, name="James Cameron", message="안녕하세요, 제임스입니다.")
    )
    repo.save_all = AsyncMock(return_value=None)
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JamesCmdInteractor(repository=mock_repository)


def _command(**overrides) -> JamesPassengerCommand:
    person_fields = dict(
        passenger_id=overrides.pop("passenger_id", "1"),
        name=overrides.pop("name", "Braund, Mr. Owen"),
        gender=overrides.pop("gender", "male"),
        age=overrides.pop("age", "22"),
        sib_sp=overrides.pop("sib_sp", "1"),
        parch=overrides.pop("parch", "0"),
        survived=overrides.pop("survived", "0"),
    )
    booking_fields = dict(
        pclass=overrides.pop("pclass", "3"),
        ticket=overrides.pop("ticket", "A/5 21171"),
        fare=overrides.pop("fare", "7.25"),
        cabin=overrides.pop("cabin", ""),
        embarked=overrides.pop("embarked", "S"),
    )
    return JamesPassengerCommand(
        person=PersonCommand(**person_fields),
        booking=BookingCommand(**booking_fields),
    )


class TestIntroduceMyself:
    async def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        query = JamesIntroduceQuery(id=4, name="James Cameron")
        await interactor.introduce_myself(query)
        mock_repository.introduce_myself.assert_called_once_with(query)

    async def test_returns_repository_response(self, interactor):
        response = await interactor.introduce_myself(JamesIntroduceQuery(id=4, name="James Cameron"))
        assert response == JamesIntroduceResult(id=4, name="James Cameron", message="안녕하세요, 제임스입니다.")


class TestExecute:
    async def test_creates_one_command_per_record(self, interactor, mock_repository):
        await interactor.execute([_command(passenger_id="1"), _command(passenger_id="2")])
        commands, = mock_repository.save_all.call_args.args
        assert len(commands) == 2

    async def test_command_contains_correct_person_fields(self, interactor, mock_repository):
        await interactor.execute([_command(passenger_id="7", gender="female", age="28")])
        commands, = mock_repository.save_all.call_args.args
        cmd = commands[0]
        assert cmd.person.passenger_id == "7"
        assert cmd.person.gender == "female"
        assert cmd.person.age == "28"

    async def test_command_contains_correct_booking_fields(self, interactor, mock_repository):
        await interactor.execute([_command(pclass="1", fare="100.0", embarked="C")])
        commands, = mock_repository.save_all.call_args.args
        cmd = commands[0]
        assert cmd.booking.pclass == "1"
        assert cmd.booking.fare == "100.0"
        assert cmd.booking.embarked == "C"

    async def test_returns_saved_count(self, interactor):
        result = await interactor.execute([_command(), _command(passenger_id="2")])
        assert result == JamesUploadResult(count=2)
