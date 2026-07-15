from __future__ import annotations

from pydantic import BaseModel


class RouteRequest(BaseModel):
    question: str


class RouteResponse(BaseModel):
    destination: str
    entities: list[str]
