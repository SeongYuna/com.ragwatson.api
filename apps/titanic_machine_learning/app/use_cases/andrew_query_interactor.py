import re

from kiwipiepy import Kiwi

from titanic_machine_learning.app.dtos.andrew_dto import (
    AndrewIntent,
    AndrewIntroduceQuery,
    AndrewIntroduceResult,
    AndrewPageQueryResult,
)
from titanic_machine_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_machine_learning.app.ports.output.andrew_port import AndrewPort

# Kiwi 인스턴스는 로딩 비용이 크므로 모듈 단위 지연 싱글턴으로 재사용한다.
_kiwi: Kiwi | None = None


def _get_kiwi() -> Kiwi:
    global _kiwi
    if _kiwi is None:
        _kiwi = Kiwi()
    return _kiwi


# 형태소 매칭 어휘
_SURVIVAL_FORMS = {"생존", "살", "살아남"}
_FEMALE_FORMS = {"여성", "여자", "여"}
_MALE_FORMS = {"남성", "남자", "남"}
_AGE_UNITS = {"세", "살"}
_CLASS_UNITS = {"등석", "등급", "등"}
_FARE_FORMS = {"요금", "운임"}

# 영어 질문 fallback
_EN_SURVIVAL = re.compile(r"surviv|would .*live", re.IGNORECASE)
_EN_AGE = re.compile(r"(\d{1,3})\s*(?:years?\s*old|yo)\b", re.IGNORECASE)
_EN_CLASS = re.compile(r"([1-3])\s*(?:st|nd|rd)?\s*class", re.IGNORECASE)
_EN_FARE = re.compile(r"fare[^\d]*(\d+)", re.IGNORECASE)


def _to_float(s: str) -> float | None:
    try:
        return float(s)
    except ValueError:
        return None


def _to_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


class AndrewQueryInteractor(AndrewUseCase):
    def __init__(self, repository: AndrewPort) -> None:
        self._repository = repository

    async def find_page(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> AndrewPageQueryResult:
        return await self._repository.find_page(skip=skip, limit=limit)

    async def analyze_intent(self, question: str) -> AndrewIntent:
        """Kiwi 형태소 분석으로 질문 의도와 승객 피처를 파악한다."""
        kiwi = _get_kiwi()
        cleaned = kiwi.space(question)
        tokens: list = list(kiwi.tokenize(cleaned))  # type: ignore[arg-type]
        forms = [t.form for t in tokens]
        nouns = tuple(t.form for t in tokens if t.tag.startswith("NN"))
        lowered = question.lower()

        # 생존 의도
        is_survival = any(f in _SURVIVAL_FORMS for f in forms) or bool(_EN_SURVIVAL.search(lowered))

        # 성별
        sex: str | None = None
        if any(f in _FEMALE_FORMS for f in forms) or "female" in lowered:
            sex = "female"
        elif any(f in _MALE_FORMS for f in forms) or re.search(r"\b(?:male|man)\b", lowered):
            sex = "male"

        # 나이·객실등급: 숫자(SN) + 단위 명사 페어링
        age: float | None = None
        pclass: int | None = None
        for i, t in enumerate(tokens):
            if t.tag != "SN":
                continue
            nxt = tokens[i + 1].form if i + 1 < len(tokens) else ""
            if nxt in _AGE_UNITS and age is None:
                age = _to_float(t.form)
            elif nxt in _CLASS_UNITS and pclass is None:
                pclass = _to_int(t.form)

        # 요금: 요금/운임 명사 뒤 첫 숫자
        fare: float | None = None
        fare_idx = next((i for i, t in enumerate(tokens) if t.form in _FARE_FORMS), None)
        if fare_idx is not None:
            for t in tokens[fare_idx + 1:]:
                if t.tag == "SN":
                    fare = _to_float(t.form)
                    break

        # 영어 fallback
        if age is None:
            m = _EN_AGE.search(lowered)
            if m:
                age = float(m.group(1))
        if pclass is None:
            m = _EN_CLASS.search(lowered)
            if m:
                pclass = int(m.group(1))
        if fare is None:
            m = _EN_FARE.search(lowered)
            if m:
                fare = float(m.group(1))

        return AndrewIntent(
            is_survival_question=is_survival,
            has_passenger_features=age is not None or sex is not None,
            sex=sex,
            age=age,
            pclass=pclass,
            fare=fare,
            sibsp=0,
            parch=0,
            nouns=nouns,
        )

    async def introduce_myself(self, query: AndrewIntroduceQuery) -> AndrewIntroduceResult:
        return await self._repository.introduce_myself(query)
