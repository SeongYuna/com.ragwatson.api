from dataclasses import dataclass


@dataclass(frozen=True)
class AndrewPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class AndrewBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class AndrewPassengerQuery:
    person: AndrewPersonQuery
    booking: AndrewBookingQuery


@dataclass(frozen=True)
class AndrewPageQueryResult:
    passengers: list[AndrewPassengerQuery]
    skip: int
    limit: int
    total: int

@dataclass(frozen=True)
class AndrewIntent:
    """프론트 질문을 Kiwi 형태소 분석으로 파악한 의도. Smith가 예측 질의로 매핑한다."""
    is_survival_question: bool        # 생존 여부를 묻는 질문인가
    has_passenger_features: bool      # 예측에 쓸 승객 피처(성별·나이)가 추출됐는가
    sex: str | None                   # "male" | "female" | None
    age: float | None
    pclass: int | None
    fare: float | None
    sibsp: int
    parch: int
    nouns: tuple[str, ...]            # 추출된 핵심 명사 (분석 근거)


@dataclass(frozen=True)
class AndrewIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class AndrewIntroduceResult:
    id: int
    name: str
    message: str
