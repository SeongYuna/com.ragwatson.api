"""타이타닉 승객 데이터 도메인 정의 (이진 분류).

1912-04-10 Southampton 출발, 1912-04-15 침몰.
6개 독립변수로 Survived(생존 여부)를 예측하는 분류 문제.
"""

from dataclasses import dataclass
from typing import Literal

ColumnRole = Literal["target", "feature", "meta"]

# CSV에 존재하는 컬럼 (Boat는 원본 Kaggle 확장 설명용; 현재 CSV에는 없음)
CSV_COLUMNS = [
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "Sex",
    "Age",
    "SibSp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
]

# 이진 분류: 종속변수
TARGET_COLUMN = "Survived"

# 학습·예측에 쓰는 6개 독립변수
FEATURE_COLUMNS = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]

# 분석·메타용 (모델 입력 제외)
OPTIONAL_COLUMNS = ["PassengerId", "Name", "Ticket", "Cabin", "Embarked"]


@dataclass(frozen=True)
class TitanicColumnSpec:
    name: str
    description: str
    role: ColumnRole


COLUMN_SPECS: tuple[TitanicColumnSpec, ...] = (
    TitanicColumnSpec(
        "Survived",
        "생존 여부 (0=사망, 1=생존)",
        "target",
    ),
    TitanicColumnSpec("Pclass", "티켓 클래스 (1=1등석, 2=2등석, 3=3등석)", "feature"),
    TitanicColumnSpec("Sex", "성별", "feature"),
    TitanicColumnSpec("Age", "나이", "feature"),
    TitanicColumnSpec("SibSp", "함께 탑승한 형제·배우자 수", "feature"),
    TitanicColumnSpec("Parch", "함께 탑승한 부모·자녀 수", "feature"),
    TitanicColumnSpec("Fare", "탑승 요금", "feature"),
    TitanicColumnSpec("PassengerId", "승객 ID", "meta"),
    TitanicColumnSpec("Name", "승객 이름", "meta"),
    TitanicColumnSpec("Ticket", "티켓 번호", "meta"),
    TitanicColumnSpec("Cabin", "객실 번호", "meta"),
    TitanicColumnSpec(
        "Embarked",
        "승선 항구 (C=Cherbourg, Q=Queenstown, S=Southampton)",
        "meta",
    ),
)
