from dataclasses import dataclass

from titanic_m_learning.domain.value_objects.titanic_vo import Gender


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
            gender=Gender.from_sex(sex),
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
        return cls(
            passenger_id=passenger_id,
            survived=survived,
            pclass=pclass,
            name=name,
            gender=Gender(gender),
            age=age,
            sib_sp=sib_sp,
            parch=parch,
            ticket=ticket,
            fare=fare,
            cabin=cabin,
            embarked=embarked,
        )
