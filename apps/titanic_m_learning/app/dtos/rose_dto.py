from dataclasses import dataclass


@dataclass(frozen=True)
class RoseColumnInfo:
    name: str
    description: str
    role: str


@dataclass(frozen=True)
class RoseDatasetInfoResult:
    columns: tuple[RoseColumnInfo, ...]

@dataclass(frozen=True)
class RosePredictQuery:
    pclass: int       # 객실 등급 (1·2·3)
    sex: str          # 성별 ("male" | "female")
    age: float        # 나이
    fare: float       # 요금
    sibsp: int        # 형제자매·배우자 수
    parch: int        # 부모·자녀 수


@dataclass(frozen=True)
class RosePredictResult:
    survived: bool
    probability: float
    algorithm: str


@dataclass(frozen=True)
class RoseIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class RoseIntroduceResult:
    id: int
    name: str
    message: str
