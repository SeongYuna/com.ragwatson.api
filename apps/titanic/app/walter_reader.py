#reader

import pandas as pd             #import 라이브러리
from pathlib import Path
import json

_Data_dir = Path(__file__).resolve().parent
_CSV_PATH = _Data_dir / "titanic_dataset.csv"

class Walter(object):               #class를 정의한다.에이전트를 구성하는 각 역할을 하는 존재.  #객체를 초기화
    def __init__(self):             #method를 정의한다. 행위, 동작. (메서드 <= 함수) instance. 데이터(상태)를 가짐
        pass                        #algoritm. 

    def get_data(self):             #brace   변수 변수값 함수 상수 데이터 
        df = pd.read_csv(_CSV_PATH)
        # 인덱스 1번 행만 반환 (DataFrame 형태 유지)
        return df.iloc[[0]].astype(object).where(df.iloc[[0]].notna(), None)

    def get_count(self):             #brace   변수 변수값 함수 상수 데이터 
        df = pd.read_csv(_CSV_PATH)
        # 전체 승객 수(총 행 개수) 반환
        return len(df)

    def get_survived_count(self):
        df = pd.read_csv(_CSV_PATH)
        # 살아남은 승객 수(Survived == 1) 총합 반환
        return int(df["Survived"].fillna(0).astype(int).sum())

    def get_dead_count(self):
        df = pd.read_csv(_CSV_PATH)
        # 사망한 승객 수(Survived == 0) 총합 반환
        return int((df["Survived"].fillna(0).astype(int) == 0).sum())