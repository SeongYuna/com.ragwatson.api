from __future__ import annotations

from pydantic import BaseModel

from starcraft_hub.domain.value_objects.route_destination import RouteDestination


class RouteQueryCommand(BaseModel):
    question: str


class RouteQueryResult(BaseModel):
    destination: RouteDestination
    entities: list[str]
