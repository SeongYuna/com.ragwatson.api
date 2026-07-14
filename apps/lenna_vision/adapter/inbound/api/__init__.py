from fastapi import APIRouter

from lenna_vision.adapter.inbound.api.v1.lenna_vision_router import lenna_vision_query_router
from lenna_vision.adapter.inbound.api.v1.yolo_router import yolo_router

lenna_vision_router = APIRouter()
lenna_vision_router.include_router(lenna_vision_query_router)
lenna_vision_router.include_router(yolo_router)
