from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from titanic_m_learning.adapter.outbound.orm.person_orm import PersonORM
from titanic_m_learning.app.dtos.smith_dto import SmithStatsResult
from titanic_m_learning.app.ports.output.smith_repository import SmithRepository
from titanic_m_learning.app.dtos.smith_dto import SmithIntroduceQuery, SmithIntroduceResult


class SmithStatsPgRepository(SmithRepository):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def fetch_summary(self) -> SmithStatsResult:
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
        return SmithStatsResult(
            total=total_count,
            survived=survived_count,
            deceased=deceased_count,
            survival_rate=survival_rate,
        )
    async def introduce_myself(self, query: SmithIntroduceQuery) -> SmithIntroduceResult:
        return SmithIntroduceResult(
            id=query.id,
            name=query.name,
            message='타이타닉 선장 Edward Smith입니다. 백만장자들의 선장이라 불렸으며, 고조되는 위기 속 배와 운명을 함께했습니다.',
        )

