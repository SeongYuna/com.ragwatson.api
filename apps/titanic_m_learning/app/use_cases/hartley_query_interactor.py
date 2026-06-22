import io
from typing import Optional

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

from titanic_m_learning.app.dtos.hartley_dto import HartleyIntroduceQuery, HartleyIntroduceResult, HartleyPassengerQuery
from titanic_m_learning.app.ports.input.hartley_use_case import HartleyUseCase
from titanic_m_learning.app.ports.output.hartley_port import HartleyPort

matplotlib.use("Agg")  # GUI 없는 서버 환경 — 반드시 pyplot import 전에 설정


class HartleyQueryInteractor(HartleyUseCase):
    def __init__(self, repository: HartleyPort) -> None:
        self._repository = repository
        self._heatmap_cache: Optional[bytes] = None  # 최초 1회 생성 후 재사용

    async def sample(self, *, count: int = 10) -> list[HartleyPassengerQuery]:
        return await self._repository.sample(count=count)

    async def introduce_myself(self, query: HartleyIntroduceQuery) -> HartleyIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def get_correlation_heatmap(self) -> bytes:
        """생존 상관관계 히트맵 PNG를 반환한다. 최초 1회 생성 후 메모리 캐시."""
        if self._heatmap_cache is not None:
            return self._heatmap_cache

        # 전체 데이터 조회 (titanic 전체 행 수 ~891보다 크게 설정)
        rows = await self._repository.sample(count=2000)

        import pandas as pd
        records = [
            {
                "survived": int(p.person.survived) if p.person.survived.isdigit() else None,
                "pclass":   int(p.booking.pclass) if p.booking.pclass.isdigit() else None,
                "age":      float(p.person.age) if _is_numeric(p.person.age) else None,
                "sibsp":    int(p.person.sib_sp) if p.person.sib_sp.isdigit() else None,
                "parch":    int(p.person.parch) if p.person.parch.isdigit() else None,
                "fare":     float(p.booking.fare) if _is_numeric(p.booking.fare) else None,
            }
            for p in rows
        ]
        df = pd.DataFrame(records).dropna()

        corr = df.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr,
            annot=True,
            cmap="coolwarm",
            fmt=".2f",
            linewidths=0.5,
            ax=ax,
        )
        ax.set_title("Titanic Survival Correlation Feature Matrix")
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=120)
        buf.seek(0)
        plt.close(fig)  # 메모리 누수 방지

        self._heatmap_cache = buf.read()
        return self._heatmap_cache


def _is_numeric(value: str) -> bool:
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
