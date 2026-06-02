from titanic_m_learning.app.ports.input.isador_use_case import IsadorUseCase
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class IsadorQuery(IsadorUseCase):
    async def find_families(self) -> list[TitanicPassenger]:
        raise NotImplementedError("Isador 가족·커플 조회는 아직 구현되지 않았습니다.")
