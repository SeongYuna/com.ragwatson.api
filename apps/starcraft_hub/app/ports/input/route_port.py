from __future__ import annotations

from abc import ABC, abstractmethod

from starcraft_hub.app.dtos.route_dto import RouteQueryCommand, RouteQueryResult


class RoutePort(ABC):
    @abstractmethod
    async def route(self, command: RouteQueryCommand) -> RouteQueryResult:
        ...
