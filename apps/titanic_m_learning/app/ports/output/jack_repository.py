from abc import ABC, abstractmethod

from titanic_m_learning.app.dtos.jack_dto import JackIntroduceQuery, JackIntroduceResult, JackPassengerQuery, JackTrainRow


class JackRepository(ABC):
    @abstractmethod
    async def find_by_id(self, passenger_id: str) -> JackPassengerQuery:
        ...

    @abstractmethod
    async def introduce_myself(self, query: JackIntroduceQuery) -> JackIntroduceResult:
        ...

    @abstractmethod
    async def fetch_all_for_training(self) -> list[JackTrainRow]:
        """ML 훈련용 전체 승객 데이터를 반환한다."""
        ...

