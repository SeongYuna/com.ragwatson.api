from __future__ import annotations

from core.lol.t1_mid_faker_orchestrator import faker_orchestrator
from starcraft_hub.app.ports.input.route_port import RoutePort
from starcraft_hub.app.use_cases.semantic_router_interactor import SemanticRouterInteractor


def get_route_use_case() -> RoutePort:
    return SemanticRouterInteractor(orchestrator=faker_orchestrator)
