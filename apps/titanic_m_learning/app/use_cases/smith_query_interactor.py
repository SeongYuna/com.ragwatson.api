import re
import logging
from typing import Optional

from titanic_m_learning.app.dtos.smith_dto import (
    SmithStatsResult,
    SmithIntroduceQuery,
    SmithIntroduceResult,
    SmithChatMessageDto,
    SmithChatQuery,
    SmithChatResult,
)
from titanic_m_learning.app.dtos.rose_dto import RosePredictQuery, RosePredictResult
from titanic_m_learning.app.ports.input.smith_use_case import SmithUseCase
from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.app.ports.input.rose_use_case import RoseUseCase
from titanic_m_learning.app.ports.input.walter_use_case import WalterUseCase
from titanic_m_learning.app.ports.input.caledon_use_case import CaledonUseCase
from titanic_m_learning.app.ports.input.lowe_use_case import LoweUseCase
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.smith_repository import SmithRepository

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# 시스템 프롬프트 템플릿
# ──────────────────────────────────────────────

_SYSTEM_PROMPT = """\
당신은 타이타닉호의 선장 에드워드 스미스(Edward Smith)입니다.
1912년 타이타닉 침몰 당시의 데이터를 ML로 분석한 결과를 바탕으로,
승객 생존 가능성을 역사적 맥락과 함께 답변합니다.

[생존율 영향 요인 — 상관관계 순위]
1. 성별(Sex)     +0.53  여성이 남성보다 생존율 훨씬 높음 ("여성과 아이 먼저")
2. 나이(Age)     -0.25  어릴수록 생존 유리
3. 운임(Fare)    +0.13  비싼 좌석일수록 구조선 접근에 유리
4. 혼승(Alone)   -0.11  가족 동반 시 구조 우선순위 상승

[훈련된 ML 모델 성능]
최우수 알고리즘: {winner}  (정확도 {winner_accuracy:.1%})
전체 알고리즘 순위:
{scores}
{prediction_block}"""

_PREDICTION_BLOCK = """\

[이번 질문의 생존 예측 결과]
  - 조건    : {condition}
  - 예측    : {verdict}
  - 생존 확률: {probability:.1%}
  - 사용 모델: {algorithm}
"""


class SmithQueryInteractor(SmithUseCase):
    def __init__(
        self,
        repository: SmithRepository,
        jack: JackUseCase,
        rose: RoseUseCase,
        walter: WalterUseCase,
        caledon: CaledonUseCase,
        lowe: LoweUseCase,
        hartley: HartleyUseCase,
    ) -> None:
        self._repository = repository
        self._jack = jack
        self._rose = rose
        self._walter = walter
        self._caledon = caledon
        self._lowe = lowe
        self._hartley = hartley

    # ──────────────────────────────────────────
    # UseCase 구현
    # ──────────────────────────────────────────

    async def get_summary(self) -> SmithStatsResult:
        return await self._repository.fetch_summary()

    async def introduce_myself(self, query: SmithIntroduceQuery) -> SmithIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def chat(self, query: SmithChatQuery) -> SmithChatResult:
        last_question = query.messages[-1].content
        logger.info("[smith/chat] question=%s", last_question[:80])

        # 1. 모델 훈련 → 평가 → 최우수 알고리즘 선택
        bundle       = await self._jack.train_model()
        model_result = await self._caledon.test_model(bundle)
        await self._hartley.get_correlation_heatmap()   # 캐시 워밍

        # 2. 생존 예측 질문이면 예측 수행
        prediction_block = ""
        predict_query = _extract_passenger_features(last_question)
        if predict_query is not None:
            result: RosePredictResult = await self._rose.predict_by_algorithm(
                predict_query, model_result.winner
            )
            condition = _describe_query(predict_query)
            verdict   = "생존 가능성 높음" if result.survived else "생존 가능성 낮음"
            prediction_block = _PREDICTION_BLOCK.format(
                condition=condition,
                verdict=verdict,
                probability=result.probability,
                algorithm=result.algorithm,
            )
            logger.info("[smith/chat] prediction=%s prob=%.2f", verdict, result.probability)

        # 3. 시스템 프롬프트 완성
        scores_text = "\n".join(
            f"  {i+1}. {s.algorithm}: 정확도 {s.accuracy:.1%}, F1 {s.f1:.3f}"
            for i, s in enumerate(
                sorted(model_result.scores, key=lambda x: x.accuracy, reverse=True)
            )
        )
        system_content = _SYSTEM_PROMPT.format(
            winner=model_result.winner,
            winner_accuracy=model_result.winner_accuracy,
            scores=scores_text,
            prediction_block=prediction_block,
        )

        # 4. Gemini 호출 (시스템 컨텍스트 + 대화 이력)
        messages = (
            SmithChatMessageDto(role="user",      content=system_content),
            SmithChatMessageDto(role="assistant", content="알겠습니다. 타이타닉 선장으로서 답변드리겠습니다."),
            *[SmithChatMessageDto(role=m.role, content=m.content) for m in query.messages],
        )
        reply = await self._repository.generate_reply(
            SmithChatQuery(messages=messages, model=query.model)
        )
        return SmithChatResult(reply=reply.reply)


# ──────────────────────────────────────────────
# 자연어 피처 추출 헬퍼
# ──────────────────────────────────────────────

_SURVIVAL_KEYWORDS = re.compile(
    r"살[았수]|생존|살아남|survived?|would.*live|survive",
    re.IGNORECASE,
)
_AGE_PATTERN   = re.compile(r"(\d{1,3})\s*(?:세|살|years?\s*old)", re.IGNORECASE)
_SEX_MALE      = re.compile(r"남자|남성|남\b|male\b", re.IGNORECASE)
_SEX_FEMALE    = re.compile(r"여자|여성|여\b|female\b", re.IGNORECASE)
_CLASS_PATTERN = re.compile(r"([1-3])\s*(?:등석|등급|class)", re.IGNORECASE)
_FARE_PATTERN  = re.compile(r"(?:요금|운임|fare)[^\d]*(\d+)", re.IGNORECASE)


def _extract_passenger_features(text: str) -> Optional[RosePredictQuery]:
    """질문에서 승객 피처를 추출한다. 생존 관련 질문이 아니거나 피처 부족이면 None."""
    if not _SURVIVAL_KEYWORDS.search(text):
        return None

    age_m  = _AGE_PATTERN.search(text)
    sex_f  = _SEX_FEMALE.search(text)
    sex_m  = _SEX_MALE.search(text)
    cls_m  = _CLASS_PATTERN.search(text)
    fare_m = _FARE_PATTERN.search(text)

    # 성별·나이 중 하나도 없으면 예측할 근거 없음
    if not age_m and not sex_m and not sex_f:
        return None

    age    = float(age_m.group(1)) if age_m else 30.0
    sex    = "female" if sex_f else "male"
    pclass = int(cls_m.group(1)) if cls_m else 3
    fare   = float(fare_m.group(1)) if fare_m else _default_fare(pclass)

    return RosePredictQuery(pclass=pclass, sex=sex, age=age, fare=fare, sibsp=0, parch=0)


def _default_fare(pclass: int) -> float:
    return {1: 80.0, 2: 20.0, 3: 8.0}.get(pclass, 8.0)


def _describe_query(q: RosePredictQuery) -> str:
    sex_label = "여성" if q.sex == "female" else "남성"
    return f"{q.age:.0f}세 {sex_label}, {q.pclass}등석, 요금 {q.fare:.0f}"
