import pandas as pd
from pathlib import Path
import json

_Data_dir = Path(__file__).resolve().parent
_CSV_PATH = _Data_dir / "doro_dataset.csv"

class DoroReader:
    def __init__(self):
        pass

    def get_data(self): 
        df = pd.read_csv(_CSV_PATH)
        return df.iloc[[1]].astype(object).where(df.iloc[[1]].notna(), None)