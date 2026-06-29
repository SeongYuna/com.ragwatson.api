from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.jack_dto import (
    JackPassengerQuery,
    JackTrainBundle,
    JackIntroduceQuery,
    JackIntroduceResult,
)


class JackUseCase(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        """passenger_id로 승객 1명을 조회한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, query: JackIntroduceQuery) -> JackIntroduceResult:
        """Jack 자기소개."""
        ...

    @abstractmethod
    async def train_model(self) -> JackTrainBundle:
        """로즈가 제안한 모델들을 훈련시키는 메소드."""
        ...
