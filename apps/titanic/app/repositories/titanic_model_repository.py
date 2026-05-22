"""rose_model.py → 학습 모델(pkl) 저장·로드 레이어."""

from pathlib import Path

from joblib import dump, load
from sklearn.tree import DecisionTreeClassifier

_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
MODEL_PATH = _DATA_DIR / "titanic_decision_tree.pkl"


class TitanicModelRepository:
    def __init__(self) -> None:
        self.model_path = MODEL_PATH
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

    def has_model(self) -> bool:
        return self.model is not None

    def get_model_name(self) -> str | None:
        if self.model is None:
            return None
        return self.model.__class__.__name__

    def save_model(self, model: DecisionTreeClassifier) -> Path:
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        dump(model, self.model_path)
        self.model = model
        return self.model_path
