from titanic_m_learning.app.ports.input.ruth_use_case import RuthUseCase
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class RuthQuery(RuthUseCase):
    async def find_first_class(self) -> list[TitanicPassenger]:
        raise NotImplementedError("Ruth 1등석 조회는 아직 구현되지 않았습니다.")
