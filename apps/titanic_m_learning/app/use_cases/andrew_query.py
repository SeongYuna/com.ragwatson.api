from titanic_m_learning.app.ports.input.andrew_use_case import AndrewUseCase
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class AndrewQuery(AndrewUseCase):
    async def find_page(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[TitanicPassenger]:
        raise NotImplementedError("Andrew 페이지 조회는 아직 구현되지 않았습니다.")
