#service
from titanic.app.walter_reader import Walter
from titanic.app.rose_model import Rose

class Jack:
    def __init__(self):
        self.w = Walter()
        self.r = Rose()

    def get_current_model_name(self) -> str | None:
        model = getattr(self.r, "model", None)
        if model is None:
            return None
        return model.__class__.__name__