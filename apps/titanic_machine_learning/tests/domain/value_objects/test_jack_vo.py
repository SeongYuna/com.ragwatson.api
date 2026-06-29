import pytest

from titanic_machine_learning.domain.value_objects.gender_vo import Gender, GenderType


class TestGender:
    def test_from_raw_male_returns_male_type(self):
        assert Gender.from_raw("male").value == GenderType.MALE

    def test_from_raw_female_returns_female_type(self):
        assert Gender.from_raw("female").value == GenderType.FEMALE

    def test_from_raw_unknown_string_raises(self):
        with pytest.raises(ValueError):
            Gender.from_raw("other")

    def test_from_raw_is_case_insensitive(self):
        assert Gender.from_raw("MALE").value == GenderType.MALE
        assert Gender.from_raw("Female").value == GenderType.FEMALE

    def test_from_raw_strips_whitespace(self):
        assert Gender.from_raw("  male  ").value == GenderType.MALE

    def test_from_raw_none_returns_unknown(self):
        assert Gender.from_raw(None).value == GenderType.UNKNOWN

    def test_to_int_female_is_1(self):
        assert Gender.from_raw("female").to_int() == 1

    def test_to_int_male_is_0(self):
        assert Gender.from_raw("male").to_int() == 0

    def test_to_int_unknown_is_minus_1(self):
        assert Gender.from_raw(None).to_int() == -1

    def test_gender_is_frozen(self):
        g = Gender.from_raw("male")
        with pytest.raises(Exception):
            g.value = GenderType.FEMALE
