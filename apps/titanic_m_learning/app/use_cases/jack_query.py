from titanic_m_learning.app.ports.input.jack_use_case import JackUseCase
from titanic_m_learning.domain.entities.titanic import TitanicPassenger


class JackQuery(JackUseCase):
    async def find_by_id(self, passenger_id: str) -> TitanicPassenger:
        raise NotImplementedError("Jack 승객 단건 조회는 아직 구현되지 않았습니다.")
