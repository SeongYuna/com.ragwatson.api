from dataclasses import dataclass

from titanic_m_learning.app.dtos.walter_dto import WalterPassengerQuery


@dataclass(frozen=True)
class TableQueryResult:
    passengers: list[WalterPassengerQuery]

    @property
    def count(self) -> int:
        return len(self.passengers)
