import logging
import sys

from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger("uvicorn.error")


def _log_layer(layer: str, user_schema: UserSchema):
    data = user_schema.model_dump()
    logger.warning("[%s] save_user 통과: %s", layer, data)
    print(f"[{layer}] save_user 통과: {data}", file=sys.stderr, flush=True)


class UserController:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        _log_layer("UserController", user_schema)
        user_service = UserService()
        user_service.save_user(user_schema)