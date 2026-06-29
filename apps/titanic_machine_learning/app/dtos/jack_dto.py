from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True)
class JackTrainRow:
    """ML 훈련에 필요한 원시 행 데이터. 컬럼명은 Lowe.feature_engineering 입력 스키마와 일치한다."""
    passenger_id: str
    name: str
    gender: str
    survived: str
    pclass: str
    age: str
    sib_sp: str
    parch: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass
class JackTrainBundle:
    """Jack이 훈련한 결과물. Caledon에게 전달된다."""
    trained_models: dict[str, Any]        # algorithm_name → fitted sklearn model
    X_test: np.ndarray                    # 표준화된 테스트 피처 (SVM·KNN·LR용)
    X_test_raw: np.ndarray                # 원본 스케일 테스트 피처 (트리 계열용)
    X_test_pca: np.ndarray                # PCA 변환 테스트 피처 (KMeans+PCA용)
    y_test: np.ndarray                    # 테스트 레이블


@dataclass(frozen=True)
class JackPersonQuery:
    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True)
class JackBookingQuery:
    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


@dataclass(frozen=True)
class JackPassengerQuery:
    person: JackPersonQuery
    booking: JackBookingQuery

@dataclass(frozen=True)
class JackIntroduceQuery:
    id: int
    name: str


@dataclass(frozen=True)
class JackIntroduceResult:
    id: int
    name: str
    message: str
