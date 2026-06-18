import pytest

from titanic_m_learning.domain.entities.titanic import TitanicPassenger
from titanic_m_learning.domain.value_objects.gender_vo import GenderType


def _make_passenger(**overrides) -> TitanicPassenger:
    defaults = dict(
        passenger_id="P001",
        survived="0",
        pclass="3",
        name="Dawson, Mr. Jack",
        sex="male",
        age="30",
        sib_sp="0",
        parch="0",
        ticket="A/5 21171",
        fare="7.25",
        cabin="",
        embarked="S",
    )
    defaults.update(overrides)
    return TitanicPassenger.create(**defaults)


class TestCreate:
    def test_passenger_id_is_set(self):
        assert _make_passenger(passenger_id="P099").passenger_id == "P099"

    def test_male_sex_maps_to_male_gender_type(self):
        assert _make_passenger(sex="male").gender.value == GenderType.MALE

    def test_female_sex_maps_to_female_gender_type(self):
        assert _make_passenger(sex="female").gender.value == GenderType.FEMALE

    def test_name_is_set(self):
        assert _make_passenger(name="Smith, Mrs. Jane").name == "Smith, Mrs. Jane"


class TestFromPersistence:
    def test_gender_female_is_preserved(self):
        p = TitanicPassenger.from_persistence(
            passenger_id="1", survived="1", pclass="1",
            name="Smith", gender=0, age="40",
            sib_sp="0", parch="0", ticket="T1",
            fare="100.0", cabin="C85", embarked="C",
        )
        assert p.gender.value == GenderType.FEMALE

    def test_gender_male_is_preserved(self):
        p = TitanicPassenger.from_persistence(
            passenger_id="2", survived="0", pclass="3",
            name="Braund", gender=1, age="22",
            sib_sp="1", parch="0", ticket="A/5",
            fare="7.25", cabin="", embarked="S",
        )
        assert p.gender.value == GenderType.MALE
