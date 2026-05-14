#controller

from fastapi import FastAPI

from titanic.app.walter_reader import Walter
from titanic.app.jack_service import Jack
from titanic.app.rose_model import Rose

app = FastAPI(title="Doro App")

class James:
    def __init__(self):
        self.w = Walter()
        self.r = Rose()
        self.j = Jack()

    def get_data(self):
        w = Walter()
        return self.w.get_data()

    def get_count(self):
        w = Walter()
        return self.w.get_count()

    def get_survived_count(self):
        w = Walter()
        return self.w.get_survived_count()

    def get_dead_count(self):
        w = Walter()
        return self.w.get_dead_count()

    def has_decision_tree_model(self):
        return self.r.model_path.exists()

    def train_decision_tree_model(self):
        return self.r.train_and_save_model()

    def get_current_model_name(self) -> str | None:
        return self.j.get_current_model_name()