import logging
import sys

from secom.app.schemas.user_schema import UserSchema
from secom.app.models.user_model import UserModel

logger = logging.getLogger("uvicorn.error")


def _log_layer(layer: str, user_schema: UserSchema):
    data = user_schema.model_dump()
    logger.warning("[%s] save_user 통과: %s", layer, data)
    print(f"[{layer}] save_user 통과: {data}", file=sys.stderr, flush=True)


class UserRepository:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        _log_layer("UserRepository", user_schema)

