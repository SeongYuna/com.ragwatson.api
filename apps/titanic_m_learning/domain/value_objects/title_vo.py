from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TitleType(int, Enum):
    MR = 1
    MISS = 2
    MRS = 3
    MASTER = 4
    ROYAL = 5
    RARE = 6
    UNKNOWN = 0


_RAW_TO_TITLE: dict[str, TitleType] = {
    "Mr":        TitleType.MR,
    "Miss":      TitleType.MISS,
    "Mrs":       TitleType.MRS,
    "Master":    TitleType.MASTER,
    # Royal
    "Countess":  TitleType.ROYAL,
    "Lady":      TitleType.ROYAL,
    "Sir":       TitleType.ROYAL,
    # Rare
    "Capt":      TitleType.RARE,
    "Col":       TitleType.RARE,
    "Don":       TitleType.RARE,
    "Dr":        TitleType.RARE,
    "Major":     TitleType.RARE,
    "Rev":       TitleType.RARE,
    "Jonkheer":  TitleType.RARE,
    "Dona":      TitleType.RARE,
    "Mme":       TitleType.RARE,
    # 정규화
    "Mlle":      TitleType.MR,
    "Ms":        TitleType.MISS,
}

_LABEL: dict[TitleType, str] = {
    TitleType.MR:      "Mr",
    TitleType.MISS:    "Miss",
    TitleType.MRS:     "Mrs",
    TitleType.MASTER:  "Master",
    TitleType.ROYAL:   "Royal",
    TitleType.RARE:    "Rare",
    TitleType.UNKNOWN: "Unknown",
}


@dataclass(frozen=True)
class Title:
    """이름에서 추출한 호칭 — 나이·성별·사회적 지위의 대리 변수.

    Rare  : Capt, Col, Don, Dr, Major, Rev, Jonkheer, Dona, Mme
    Royal : Countess, Lady, Sir
    정규화 : Mlle → Mr / Ms → Miss
    """

    value: TitleType

    @classmethod
    def from_name(cls, name: Optional[str]) -> "Title":
        """이름 문자열에서 호칭을 추출한다."""
        if name is None or name.strip() == "":
            return cls(value=TitleType.UNKNOWN)
        match = re.search(r"([A-Za-z]+)\.", name)
        if not match:
            return cls(value=TitleType.UNKNOWN)
        raw = match.group(1)
        return cls(value=_RAW_TO_TITLE.get(raw, TitleType.UNKNOWN))

    @classmethod
    def from_int(cls, code: Optional[int]) -> "Title":
        """ML 인코딩 정수값으로 복원한다."""
        if code is None:
            return cls(value=TitleType.UNKNOWN)
        try:
            return cls(value=TitleType(code))
        except ValueError:
            return cls(value=TitleType.UNKNOWN)

    @property
    def label(self) -> str:
        return _LABEL[self.value]

    @property
    def is_royal(self) -> bool:
        return self.value == TitleType.ROYAL

    @property
    def is_rare(self) -> bool:
        return self.value == TitleType.RARE

    @property
    def is_unknown(self) -> bool:
        return self.value == TitleType.UNKNOWN

    def to_int(self) -> int:
        """ML 인코딩: Mr=1, Miss=2, Mrs=3, Master=4, Royal=5, Rare=6, Unknown=0"""
        return self.value.value

    def __str__(self) -> str:
        return self.label
