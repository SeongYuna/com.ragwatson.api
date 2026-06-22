from titanic_m_learning.app.dtos.rose_dto import RoseColumnInfo, RoseDatasetInfoResult
from titanic_m_learning.app.ports.output.rose_port import RosePort
from titanic_m_learning.app.dtos.rose_dto import RoseIntroduceQuery, RoseIntroduceResult

_TITANIC_COLUMNS: tuple[RoseColumnInfo, ...] = (
    RoseColumnInfo(name="PassengerId", description="승객 ID", role="identifier"),
    RoseColumnInfo(name="Survived", description="생존 여부 (0/1)", role="target"),
    RoseColumnInfo(name="Pclass", description="객실 등급", role="feature"),
    RoseColumnInfo(name="Name", description="승객 이름", role="feature"),
    RoseColumnInfo(name="Sex", description="성별", role="feature"),
    RoseColumnInfo(name="Age", description="나이", role="feature"),
    RoseColumnInfo(name="SibSp", description="형제·배우자 수", role="feature"),
    RoseColumnInfo(name="Parch", description="부모·자녀 수", role="feature"),
    RoseColumnInfo(name="Ticket", description="티켓 번호", role="feature"),
    RoseColumnInfo(name="Fare", description="요금", role="feature"),
    RoseColumnInfo(name="Cabin", description="선실", role="feature"),
    RoseColumnInfo(name="Embarked", description="탑승 항구", role="feature"),
)


class RoseQueryRepository(RosePort):
    async def fetch_dataset_info(self) -> RoseDatasetInfoResult:
        return RoseDatasetInfoResult(columns=_TITANIC_COLUMNS)

    async def introduce_myself(self, query: RoseIntroduceQuery) -> RoseIntroduceResult:
        return RoseIntroduceResult(
            id=query.id,
            name=query.name,
            message="Rose DeWitt Bukater입니다. 타이타닉 데이터셋 컬럼 메타정보를 제공합니다.",
        )

