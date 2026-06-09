from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.caledon_dto import CaledonStatsResult
from titanic_m_learning.app.ports.output.caledon_repository import CaledonRepository
from titanic_m_learning.app.dtos.caledon_dto import CaledonIntroduceQuery, CaledonIntroduceResult


class CaledonStatsPgRepository(CaledonRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def fetch_stats(self) -> CaledonStatsResult:
        total = await self._db.scalar(select(func.count()).select_from(PersonORM))
        survived = await self._db.scalar(
            select(func.count())
            .select_from(PersonORM)
            .where(PersonORM.survived == "1")
        )
        total_count = int(total or 0)
        survived_count = int(survived or 0)
        deceased_count = total_count - survived_count
        survival_rate = survived_count / total_count if total_count else 0.0
        return CaledonStatsResult(
            total=total_count,
            survived=survived_count,
            deceased=deceased_count,
            survival_rate=survival_rate,
        )
    async def introduce_myself(self, query: CaledonIntroduceQuery) -> CaledonIntroduceResult:
        return CaledonIntroduceResult(
            id=query.id,
            name=query.name,
            message='Caledon Hockley입니다.',
        )

