from dataclasses import dataclass

_SEX_TO_GENDER = {"male": 1, "female": 0}


@dataclass(frozen=True)
class Gender:
    """0=female, 1=male, -1=unknown"""

    value: int

    @classmethod
    def from_sex(cls, sex: str) -> "Gender":
        return cls(_SEX_TO_GENDER.get(sex.strip().lower(), -1))
