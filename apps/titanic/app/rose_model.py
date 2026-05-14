#model

from pathlib import Path

import pandas as pd
from joblib import load
from sklearn.tree import DecisionTreeClassifier


class Rose:
    def __init__(self):
        data_dir = Path(__file__).resolve().parent
        self.model_path = data_dir / "titanic_decision_tree.pkl"

        # Association: Rose "has a" decision-tree model instance.
        self.model: DecisionTreeClassifier | None = self._load_model(self.model_path)

    def _load_model(self, path: Path) -> DecisionTreeClassifier | None:
        if not path.exists():
            return None
        obj = load(path)
        if isinstance(obj, DecisionTreeClassifier):
            return obj
        if isinstance(obj, dict) and isinstance(obj.get("model"), DecisionTreeClassifier):
            return obj["model"]
        return None

    def get_current_model_name(self) -> str | None:
        if self.model is None:
            return None
        return self.model.__class__.__name__
        