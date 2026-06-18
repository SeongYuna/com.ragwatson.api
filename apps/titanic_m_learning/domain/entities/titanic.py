from dataclasses import dataclass

from titanic_m_learning.domain.value_objects.gender_vo import Gender, GenderType


@dataclass(frozen=True)
class TitanicPassenger:
    passenger_id: str
    survived: str
    pclass: str
    name: str
    gender: Gender
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str

    @classmethod
    def create(
        cls,
        *,
        passenger_id: str,
        survived: str,
        pclass: str,
        name: str,
        sex: str,
        age: str,
        sib_sp: str,
        parch: str,
        ticket: str,
        fare: str,
        cabin: str,
        embarked: str,
    ) -> "TitanicPassenger":
        return cls(
            passenger_id=passenger_id,
            survived=survived,
            pclass=pclass,
            name=name,
            gender=Gender.from_raw(sex),
            age=age,
            sib_sp=sib_sp,
            parch=parch,
            ticket=ticket,
            fare=fare,
            cabin=cabin,
            embarked=embarked,
        )

    @classmethod
    def from_persistence(
        cls,
        *,
        passenger_id: str,
        survived: str,
        pclass: str,
        name: str,
        gender: int,
        age: str,
        sib_sp: str,
        parch: str,
        ticket: str,
        fare: str,
        cabin: str,
        embarked: str,
    ) -> "TitanicPassenger":
        # 0 → FEMALE, 1 → MALE, 그 외 → UNKNOWN
        gender_type = {0: GenderType.FEMALE, 1: GenderType.MALE}.get(gender, GenderType.UNKNOWN)
        return cls(
            passenger_id=passenger_id,
            survived=survived,
            pclass=pclass,
            name=name,
            gender=Gender(value=gender_type),
            age=age,
            sib_sp=sib_sp,
            parch=parch,
            ticket=ticket,
            fare=fare,
            cabin=cabin,
            embarked=embarked,
        )
