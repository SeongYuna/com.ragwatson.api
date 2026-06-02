from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class HartleyQuery(HartleyUseCase):
    async def sample(self, *, count: int = 10) -> list[TitanicPassenger]:
        raise NotImplementedError("Hartley 무작위 샘플 조회는 아직 구현되지 않았습니다.")
