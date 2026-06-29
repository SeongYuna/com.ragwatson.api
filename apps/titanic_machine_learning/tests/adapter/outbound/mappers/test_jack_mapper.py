from types import SimpleNamespace

from titanic_machine_learning.adapter.outbound.mappers.jack_orm_mapper import person_booking_to_jack_query


def _make_person(**overrides):
    defaults = dict(
        passenger_id="P001",
        name="Dawson, Mr. Jack",
        gender="male",
        age="30",
        sib_sp="0",
        parch="0",
        survived="0",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def _make_booking(**overrides):
    defaults = dict(
        pclass="3",
        ticket="A/5 21171",
        fare="7.25",
        cabin="",
        embarked="S",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


class TestPersonBookingToJackQuery:
    def test_maps_passenger_id(self):
        result = person_booking_to_jack_query(_make_person(passenger_id="P099"), _make_booking())
        assert result.person.passenger_id == "P099"

    def test_maps_name(self):
        result = person_booking_to_jack_query(_make_person(name="Smith, Mr. John"), _make_booking())
        assert result.person.name == "Smith, Mr. John"

    def test_maps_gender(self):
        result = person_booking_to_jack_query(_make_person(gender="female"), _make_booking())
        assert result.person.gender == "female"

    def test_maps_age(self):
        result = person_booking_to_jack_query(_make_person(age="25"), _make_booking())
        assert result.person.age == "25"

    def test_maps_sib_sp_and_parch(self):
        result = person_booking_to_jack_query(_make_person(sib_sp="2", parch="3"), _make_booking())
        assert result.person.sib_sp == "2"
        assert result.person.parch == "3"

    def test_maps_survived(self):
        result = person_booking_to_jack_query(_make_person(survived="1"), _make_booking())
        assert result.person.survived == "1"

    def test_maps_pclass(self):
        result = person_booking_to_jack_query(_make_person(), _make_booking(pclass="1"))
        assert result.booking.pclass == "1"

    def test_maps_fare(self):
        result = person_booking_to_jack_query(_make_person(), _make_booking(fare="100.0"))
        assert result.booking.fare == "100.0"

    def test_maps_embarked(self):
        result = person_booking_to_jack_query(_make_person(), _make_booking(embarked="C"))
        assert result.booking.embarked == "C"
