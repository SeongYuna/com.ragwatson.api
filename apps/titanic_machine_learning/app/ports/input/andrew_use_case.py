from abc import ABC, abstractmethod

from titanic_machine_learning.app.dtos.andrew_dto import (
    AndrewIntent,
    AndrewPageQueryResult,
    AndrewIntroduceQuery,
    AndrewIntroduceResult,
)


class AndrewUseCase(ABC):
    @abstractmethod
    async def find_page(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> AndrewPageQueryResult:
        """탑승객 목록을 페이지 단위 Query DTO로 조회한다."""
        ...

    @abstractmethod
    async def analyze_intent(self, question: str) -> AndrewIntent:
        """Kiwi 형태소 분석으로 프론트 질문의 의도와 승객 피처를 파악한다."""
        ...

    @abstractmethod
    async def introduce_myself(self, query: AndrewIntroduceQuery) -> AndrewIntroduceResult:
        """Andrew 자기소개."""
        ...
