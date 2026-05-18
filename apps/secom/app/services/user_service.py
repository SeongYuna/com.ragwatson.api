import logging
import sys

from secom.app.schemas.user_schema import UserSchema
from secom.app.repositories.user_repository import UserRepository

logger = logging.getLogger("uvicorn.error")


def _log_layer(layer: str, user_schema: UserSchema):
    data = user_schema.model_dump()
    logger.warning("[%s] save_user 통과: %s", layer, data)
    print(f"[{layer}] save_user 통과: {data}", file=sys.stderr, flush=True)


class UserService:
    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        _log_layer("UserService", user_schema)
        user_repository = UserRepository()
        user_repository.save_user(user_schema)